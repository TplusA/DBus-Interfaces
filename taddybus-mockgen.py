#! /usr/bin/env python3

#
# Copyright (C) 2022  T+A elektroakustik GmbH & Co. KG
#
# This file is part of T+A-D-Bus.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.
#

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
import sys
import re


if sys.version_info >= (3, 9, 0):
    def _remove_prefix(s, p):
        return s.removeprefix(p)
else:
    def _remove_prefix(s, p):
        return s[len(p):] if s.startswith(p) else s


def _mk_include_guard(options):
    if options['include_guard']:
        return options['include_guard']

    if options['output_hh']:
        return options['output_hh'].name.upper().replace('.', '_')

    return 'MOCK_DBUS_' + options['FILE'].stem.upper() + '_HH'


def _write_header_top(hhfile, include_guard, mocked_header, namespace):
    template = """//
// Generated by taddybus-mockgen.
// Do not modify!
//

#ifndef {}
#define {}

#include "dbus/{}"
#include "mock_dbus_utils.hh"
#include "mock_expectation.hh"

namespace {}
{{"""
    print(template.format(include_guard, include_guard, mocked_header,
                          namespace),
          file=hhfile)


def _write_header_bottom(hhfile, include_guard):
    template = """
extern Mock *singleton;

}}

#endif /* !{} */"""
    print(template.format(include_guard), file=hhfile)


def _to_snake_case(name, divider='_'):
    return divider.join(re.findall(R'[A-Z]+$|[A-Z]*[a-z]+', name)).lower()


def _method_name(iface_type, name, is_call=False):
    return _to_snake_case(iface_type) + '_' + name + ('()' if is_call else '')


def _map_simple_type_to_ctype(typespec):
    dbus_type_to_ctype = {
        "b": "gboolean",
        "d": "gdouble",
        "i": "gint",
        "n": "gint16",
        "o": "const gchar *",
        "q": "guint16",
        "s": "const gchar *",
        "t": "guint64",
        "u": "guint",
        "v": "GVariant *",
        "x": "gint64",
        "y": "guchar"
    }

    ctype = dbus_type_to_ctype.get(typespec, None)
    if ctype and ctype[-1] != '*':
        return ctype + ' '
    else:
        return ctype


def _type_is_pointer(param):
    return param.attrib['type'][0] in ('s', 'o', 'v', 'a')


def _type_is_string(param):
    return param.attrib['type'] in ('s', 'o')


def _type_is_float(param):
    return param.attrib['type'] == 'd'


def _type_is_gvariant(param):
    return param.attrib['type'][0] in ('v', 'a')


def _map_simple_type_to_cptrtype(typespec):
    dbus_type_to_ctype = {
        "b": "gboolean *",
        "d": "gdouble *",
        "i": "gint *",
        "n": "gint16 *",
        "o": "gchar **",
        "q": "guint16 *",
        "s": "gchar **",
        "t": "guint64 *",
        "u": "guint *",
        "v": "GVariant **",
        "x": "gint64 *",
        "y": "guchar *"
    }

    ctype = dbus_type_to_ctype.get(typespec, None)
    if ctype and ctype[-1] != '*':
        return ctype + ' '
    else:
        return ctype


def _map_simple_type_to_ctortype(typespec):
    dbus_type_to_cpptype = {
        "b": "gboolean",
        "d": "gdouble",
        "i": "gint",
        "n": "gint16",
        "o": "std::string &&",
        "q": "guint16",
        "s": "std::string &&",
        "t": "guint64",
        "u": "guint",
        "v": "GVariant *",
        "x": "gint64",
        "y": "guchar"
    }

    ctype = dbus_type_to_cpptype.get(typespec, None)
    if ctype and ctype[-1] != '*' and ctype[-1] != '&':
        return ctype + ' '
    else:
        return ctype


def _map_simple_type_to_memtype(typespec):
    dbus_type_to_cpptype = {
        "b": "gboolean",
        "d": "gdouble",
        "i": "gint",
        "n": "gint16",
        "o": "std::string",
        "q": "guint16",
        "s": "std::string",
        "t": "guint64",
        "u": "guint",
        "v": "GVariant *",
        "x": "gint64",
        "y": "guchar"
    }

    ctype = dbus_type_to_cpptype.get(typespec, None)
    if ctype and ctype[-1] != '*' and ctype[-1] != '&':
        return ctype + ' '
    else:
        return ctype


def _map_simple_type_to_const_memtype(typespec):
    ctype = _map_simple_type_to_memtype(typespec)
    if ctype and typespec not in ('v', 'a'):
        ctype = 'const ' + ctype
    return ctype


def _skip_parameter(param, is_method, need_return_types):
    if is_method:
        dir = param.attrib.get('direction', 'in')

        if (need_return_types and dir == 'in') or \
                (not need_return_types and dir != 'in'):
            return True

    return False


def _mk_argument_list(params, is_method, mapping_fn, *,
                      need_return_types=False, append_to_name='',
                      need_prefixed_names=True):
    args = []

    for param in params.findall('arg'):
        if _skip_parameter(param, is_method, need_return_types):
            continue

        if need_prefixed_names:
            argname = 'out_' if need_return_types else 'arg_'
        else:
            argname = ''

        argname += param.attrib['name'] + append_to_name
        type = None

        for anno in param.findall('annotation'):
            if anno.attrib['name'] == 'org.gtk.GDBus.C.ForceGVariant' and \
                    anno.attrib['value'] == 'arg':
                type = param.attrib['type']
                is_array = True
                break

        if not type:
            type = param.attrib['type']
            is_array = type[0] == 'a'

        if is_array:
            t = mapping_fn('v') + argname + ' /* ' + type + ' */'
        else:
            t = mapping_fn(type[0])
            t += argname

        args.append(t)

    return args


def _format_string_list(args, indent=0, *,
                        leading_sep=None, leading_indent=True,
                        terminator=None):
    if not args:
        return ''

    spaces = ' ' * indent
    result = leading_sep if leading_sep else ''
    result += ('\n' + spaces) if leading_indent else ''

    if terminator:
        result += \
            (terminator + ('\n' if indent > 0 else ' ') + spaces).join(args)
        result += terminator
    else:
        result += (',' + ('\n' if indent > 0 else ' ') + spaces).join(args)

    return result


def _mk_initializer_list(params, is_method, *, need_return_types=False,
                         need_prefixed_names=True):
    statements = []

    for param in params.findall('arg'):
        if _skip_parameter(param, is_method, need_return_types):
            continue

        if need_prefixed_names:
            argname = 'out_' if need_return_types else 'arg_'
        else:
            argname = ''

        argname += param.attrib['name']

        if _type_is_gvariant(param):
            statements.append(argname + '_(std::move(g_variant_ref_sink(' +
                              argname + ')))')
        else:
            statements.append(argname + '_(std::move(' + argname + '))')

    return statements


def _mk_cleanup_statements(params, is_method, *, need_return_types,
                           need_prefixed_names=True):
    statements = []

    for param in params.findall('arg'):
        if _skip_parameter(param, is_method, need_return_types):
            continue

        if need_return_types and _type_is_pointer(param) and \
                not _type_is_string(param):
            if need_prefixed_names:
                argname = 'out_' + param.attrib['name']
            else:
                argname = param.attrib['name']

            statements.append('if(' + argname + '_ != nullptr) '
                              'g_variant_unref(' + argname + '_)')
            statements.append(argname + '_ = nullptr')
        elif not need_return_types and _type_is_gvariant(param):
            if need_prefixed_names:
                argname = 'arg_' + param.attrib['name']
            else:
                argname = param.attrib['name']

            statements.append('if(' + argname + '_ != nullptr) '
                              'g_variant_unref(' + argname + '_)')
            statements.append(argname + '_ = nullptr')

    return statements


def _mk_check_statements(params, is_method, *, need_return_types=False,
                         need_prefixed_names=True):
    statements = []

    for param in params.findall('arg'):
        if _skip_parameter(param, is_method, need_return_types):
            continue

        if need_prefixed_names:
            argname = 'out_' if need_return_types else 'arg_'
        else:
            argname = ''

        argname += param.attrib['name']

        if _type_is_pointer(param):
            if _type_is_string(param):
                statements.append(
                    'if(' + argname + '_.empty() && ' + argname +
                    ' != nullptr && ' + argname +
                    '[0] != \'\\0\') FAIL_CHECK("Argument ' + argname +
                    ' expected to be empty")')
                statements.append(
                    'else if(!' + argname + '_.empty()) CHECK(' +
                    argname + ' != nullptr)')
            else:
                statements.append(
                    'if(' + argname + '_ != nullptr) CHECK(' + argname +
                    ' != nullptr)')
                statements.append('else CHECK(' + argname + ' == nullptr)')

        use_default_checks = True

        for check_fn in param.findall('mock_check_fn'):
            use_default_checks = False
            statements.append(
                'if(' + argname + '_ != nullptr) ' + check_fn.attrib['name'] +
                '(const_cast<GVariant *>(' + argname + '), ' +
                'const_cast<GVariant *>(' + argname + '_))')

        if not use_default_checks:
            continue

        if _type_is_string(param):
            statements.append(
                'if(' + argname + ' != nullptr) CHECK(std::string(' +
                argname + ') == ' + argname + '_)')
            statements.append(
                'else CHECK(' + argname + '_.empty())')
        elif _type_is_float(param):
            statements.append('CHECK(' + argname + ' <= ' + argname + '_)')
            statements.append('CHECK(' + argname + ' >= ' + argname + '_)')
        else:
            statements.append('CHECK(' + argname + ' == ' + argname + '_)')

    return statements


def _mk_copy_statements(params, is_method, *, need_return_types=False,
                        need_prefixed_names=True):
    statements = []

    for param in params.findall('arg'):
        if _skip_parameter(param, is_method, need_return_types):
            continue

        if need_prefixed_names:
            argname = 'out_' if need_return_types else 'arg_'
        else:
            argname = ''

        argname += param.attrib['name']
        if _type_is_string(param):
            statements.append('*' + argname +
                              ' = g_strdup(' + argname + '_.c_str())')
        elif _type_is_gvariant(param):
            statements.append('if(' + argname + ' != nullptr) *' + argname +
                              ' = g_variant_ref(' + argname + '_)')
        else:
            statements.append('if(' + argname + ' != nullptr) *' + argname +
                              ' = ' + argname + '_')

    return statements


def _write_method_call_expectation(hhfile, iface_name, iface_name_stripped,
                                   iface_type, method):
    template_call = """// Expecting async method call: {}
class {}: public Expectation
{{""""""{}{}
  public:
    GCancellable *observed_cancellable_;
    GAsyncReadyCallback observed_async_ready_callback_;
    gpointer observed_user_data_;

    explicit {}({}):
        Expectation("{}"){}
    {{}}

    ~{}()
    {{
        if(observed_cancellable_ != nullptr)
            g_object_unref(observed_cancellable_);{}
    }}

    void check({} *proxy, GCancellable *cancellable, GAsyncReadyCallback callback, gpointer user_data{})
    {{
        CHECK(proxy == proxy_pointer());
        if(cancellable != nullptr)
            g_object_ref(cancellable);
        observed_cancellable_ = cancellable;
        observed_async_ready_callback_ = callback;
        observed_user_data_ = user_data;{}
    }}

    void async_ready()
    {{
        REQUIRE(observed_async_ready_callback_ != nullptr);
        observed_async_ready_callback_(
                    reinterpret_cast<GObject *>(proxy_pointer()),
                    async_result_pointer(), observed_user_data_);
    }}

    void async_ready_ignored()
    {{
        REQUIRE(observed_async_ready_callback_ == nullptr);
        REQUIRE(observed_user_data_ == nullptr);
        REQUIRE(observed_cancellable_ == nullptr);
    }}
}};
"""
    class_name = method.attrib['name']
    members = _mk_argument_list(method, True,
                                _map_simple_type_to_const_memtype,
                                append_to_name='_')
    ctor_args = _mk_argument_list(method, True, _map_simple_type_to_ctortype)
    check_args = _mk_argument_list(method, True, _map_simple_type_to_ctype)
    ctor_init = _mk_initializer_list(method, True)
    ctor_init += [
        'observed_cancellable_(nullptr)',
        'observed_async_ready_callback_(nullptr)',
        'observed_user_data_(nullptr)',
    ]
    cleanup_statements = \
        _mk_cleanup_statements(method, True, need_return_types=False)
    checks = _mk_check_statements(method, True)
    print(template_call.format(
            iface_name + '.' + method.attrib['name'], class_name,
            '\n  private:' if members else '',
            _format_string_list(members, 4, terminator=';') +
            ('\n' if members else ''),
            class_name,
            _format_string_list(ctor_args, 0, leading_indent=False),
            class_name,
            _format_string_list(ctor_init, 8, leading_sep=','),
            class_name,
            _format_string_list(cleanup_statements, 8, terminator=';'),
            iface_type,
            _format_string_list(check_args, 0,
                                leading_sep=', ', leading_indent=False),
            _format_string_list(checks, 8, terminator=';')),
          file=hhfile)

    template_finish = """// Expecting async method finish: {}
class {}: public Expectation
{{
  private:
    GError *dbus_call_error_;{}

  public:
    GAsyncResult *observed_async_result_;

    explicit {}({}):
        Expectation("{}"){}
    {{}}

    ~{}()
    {{
        if(dbus_call_error_ != nullptr) g_error_free(dbus_call_error_);
        dbus_call_error_ = nullptr;{}
    }}

    gboolean check({} *proxy{}, GAsyncResult *res, GError **error)
    {{
        CHECK(proxy == proxy_pointer());
        CHECK(res != nullptr);
        observed_async_result_ = res;

        if(dbus_call_error_ != nullptr)
        {{
            *error = dbus_call_error_;
            dbus_call_error_ = nullptr;
            return FALSE;
        }}
{}
        *error = nullptr;
        return TRUE;
    }}
}};
"""
    class_name = method.attrib['name'] + 'Finish'
    members = _mk_argument_list(method, True, _map_simple_type_to_memtype,
                                need_return_types=True, append_to_name='_')
    ctor_args = ['GError *dbus_call_error']
    ctor_args += _mk_argument_list(method, True, _map_simple_type_to_ctortype,
                                   need_return_types=True)
    check_args = _mk_argument_list(method, True, _map_simple_type_to_cptrtype,
                                   need_return_types=True)
    ctor_init = ['dbus_call_error_(std::move(dbus_call_error))']
    ctor_init += _mk_initializer_list(method, True,
                                      need_return_types=True)
    ctor_init += ['observed_async_result_(nullptr)']
    cleanup_statements = \
        _mk_cleanup_statements(method, True, need_return_types=True)
    checks = _mk_copy_statements(method, True, need_return_types=True)
    print(template_finish.format(
            iface_name + '.' + method.attrib['name'], class_name,
            _format_string_list(members, 4, terminator=';'),
            class_name,
            _format_string_list(ctor_args, 0, leading_indent=False),
            class_name,
            _format_string_list(ctor_init, 8, leading_sep=','),
            class_name,
            _format_string_list(cleanup_statements, 8, terminator=';'),
            iface_type,
            _format_string_list(check_args, 0,
                                leading_sep=', ', leading_indent=False),
            _format_string_list(checks, 8, terminator=';')),
          file=hhfile)

    template_complete = """// Expecting async method completion: {}
class {}: public Expectation
{{
  private:{}

  public:
    explicit {}({}):
        Expectation("{}"){}
    {{}}

    ~{}()
    {{""""""{}
    }}

    void check({} *object, GDBusMethodInvocation *invocation{})
    {{
        CHECK(object == proxy_pointer());
        CHECK(invocation == invocation_pointer());{}
    }}
}};
"""
    class_name = method.attrib['name'] + 'Complete'
    members = _mk_argument_list(method, True, _map_simple_type_to_memtype,
                                need_return_types=True, append_to_name='_',
                                need_prefixed_names=False)
    ctor_args = _mk_argument_list(method, True, _map_simple_type_to_ctortype,
                                  need_return_types=True,
                                  need_prefixed_names=False)
    ctor_init = _mk_initializer_list(method, True, need_return_types=True,
                                     need_prefixed_names=False)
    cleanup_statements = \
        _mk_cleanup_statements(method, True, need_return_types=True,
                               need_prefixed_names=False)
    check_args = _mk_argument_list(method, True, _map_simple_type_to_ctype,
                                   need_return_types=True,
                                   need_prefixed_names=False)
    checks = _mk_check_statements(method, True, need_return_types=True,
                                  need_prefixed_names=False)
    print(template_complete.format(
            iface_name + '.' + method.attrib['name'], class_name,
            _format_string_list(members, 4, terminator=';'),
            class_name,
            _format_string_list(ctor_args, 0, leading_indent=False),
            class_name,
            _format_string_list(ctor_init, 8, leading_sep=','),
            class_name,
            _format_string_list(cleanup_statements, 8, terminator=';'),
            iface_type,
            _format_string_list(check_args, 0,
                                leading_sep=', ', leading_indent=False),
            _format_string_list(checks, 8, terminator=';')),
          file=hhfile)


def _write_header_body(hhfile, iface_prefix, c_namespace, cpp_namespace,
                       dummy_pointer_value, iface):
    template = """
static constexpr unsigned long PROXY_POINTER_PATTERN = {};
static constexpr unsigned long ASYNC_RESULT_PATTERN = {};
static constexpr unsigned long METHOD_INVOCATION_PATTERN = {};

static inline auto *proxy_pointer()
{{
    return reinterpret_cast<{} *>(PROXY_POINTER_PATTERN);
}}

static inline GAsyncResult *async_result_pointer()
{{
    return reinterpret_cast<GAsyncResult *>(ASYNC_RESULT_PATTERN);
}}

static inline GDBusMethodInvocation *invocation_pointer()
{{
    return reinterpret_cast<GDBusMethodInvocation *>(METHOD_INVOCATION_PATTERN);
}}

/*! Base class for expectations. */
class Expectation
{{
  private:
    std::string name_;
    unsigned int sequence_serial_;

  public:
    Expectation(const Expectation &) = delete;
    Expectation(Expectation &&) = default;
    Expectation &operator=(const Expectation &) = delete;
    Expectation &operator=(Expectation &&) = default;
    Expectation(std::string &&name):
        name_(std::move(name)),
        sequence_serial_(std::numeric_limits<unsigned int>::max())
    {{}}
    virtual ~Expectation() {{}}
    const std::string &get_name() const {{ return name_; }}
    void set_sequence_serial(unsigned int ss) {{ sequence_serial_ = ss; }}
    unsigned int get_sequence_serial() const {{ return sequence_serial_; }}
}};

class Mock
{{
  private:
    MockExpectationsTemplate<Expectation> expectations_;

  public:
    Mock(const Mock &) = delete;
    Mock &operator=(const Mock &) = delete;

    explicit Mock():
        expectations_("{}")
    {{}}

    ~Mock() {{}}

    void expect(std::unique_ptr<Expectation> expectation)
    {{
        expectations_.add(std::move(expectation));
    }}

    void expect(Expectation *expectation)
    {{
        expectations_.add(std::unique_ptr<Expectation>(expectation));
    }}

    template <typename T, typename ... Args>
    T &expect(Args ... args)
    {{
        return *static_cast<T *>(expectations_.add(std::make_unique<T>(args...)));
    }}

    template <typename T>
    void ignore(std::unique_ptr<T> default_result)
    {{
        expectations_.ignore<T>(std::move(default_result));
    }}

    template <typename T>
    void ignore(T *default_result)
    {{
        expectations_.ignore<T>(std::unique_ptr<Expectation>(default_result));
    }}

    template <typename T>
    void allow() {{ expectations_.allow<T>(); }}

    void done() const {{ expectations_.done(); }}

    template <typename T, typename ... Args>
    auto check_next(Args ... args) -> decltype(std::declval<T>().check(args...))
    {{
        return expectations_.check_and_advance<T, decltype(std::declval<T>().check(args...))>(args...);
    }}

    template <typename T>
    const T &next(const char *caller) {{ return expectations_.next<T>(caller); }}
}};

"""
    iface_name = iface.attrib['name']
    iface_name_stripped = _remove_prefix(iface_name, iface_prefix)
    iface_type = c_namespace.replace('_', '') + iface_name_stripped
    print(template.format(dummy_pointer_value,
                          hex(int(dummy_pointer_value, 0) + 1),
                          hex(int(dummy_pointer_value, 0) + 2),
                          iface_type, cpp_namespace),
          file=hhfile)

    for method in iface.findall('method'):
        _write_method_call_expectation(hhfile, iface_name, iface_name_stripped,
                                       iface_type, method)

    # for signal in iface.findall('signal'):
    #     _write_signal_emit_expectation(hhfile, iface_name, signal)


def _write_impl_top(ccfile, mock_header_name):
    template = """//
// Generated by taddybus-mockgen.
// Do not modify!
//

#if HAVE_CONFIG_H
#include <config.h>
#endif /* HAVE_CONFIG_H */

#include "{}"
"""
    print(template.format(mock_header_name), file=ccfile)


def _mk_call_parameter_list(params, is_method, *, need_return_types=False,
                            need_prefixed_names=True):
    names = []

    for param in params.findall('arg'):
        if _skip_parameter(param, is_method, need_return_types):
            continue

        if need_prefixed_names:
            argname = 'out_' if need_return_types else 'arg_'
        else:
            argname = ''

        argname += param.attrib['name']
        names.append(argname)

    return names


def _write_method_call_mocks(ccfile, iface_name, iface_type, cpp_namespace,
                             fn_prefix, method):
    template = """
// Mock functions for method call: {}
void {}({} *proxy{}, GCancellable *cancellable, GAsyncReadyCallback callback, gpointer user_data)
{{
    REQUIRE({}::singleton != nullptr);
    {}::singleton->check_next<{}::{}>(proxy, cancellable, callback, user_data{});
}}

gboolean {}({} *proxy{}, GAsyncResult *res, GError **error)
{{
    REQUIRE({}::singleton != nullptr);
    CHECK(res == {}::async_result_pointer());
    return {}::singleton->check_next<{}::{}>(proxy{}, res, error);
}}"""
    call_fn_args = _mk_argument_list(method, True, _map_simple_type_to_ctype)
    call_forward_args = _mk_call_parameter_list(method, True)
    finish_fn_args = _mk_argument_list(method, True,
                                       _map_simple_type_to_cptrtype,
                                       need_return_types=True)
    finish_forward_args = _mk_call_parameter_list(method, True,
                                                  need_return_types=True)
    print(template.format(
            iface_name + '.' + method.attrib['name'],
            _method_name(fn_prefix,
                         'call_' + _to_snake_case(method.attrib['name'])),
            iface_type,
            _format_string_list(call_fn_args, 0,
                                leading_sep=', ', leading_indent=False),
            cpp_namespace, cpp_namespace, cpp_namespace, method.attrib['name'],
            _format_string_list(call_forward_args, 0,
                                leading_sep=', ', leading_indent=False),

            _method_name(fn_prefix,
                         'call_' + _to_snake_case(method.attrib['name']) +
                         '_finish'),
            iface_type,
            _format_string_list(finish_fn_args, 0,
                                leading_sep=', ', leading_indent=False),
            cpp_namespace, cpp_namespace, cpp_namespace, cpp_namespace,
            method.attrib['name'] + 'Finish',
            _format_string_list(finish_forward_args, 0,
                                leading_sep=', ', leading_indent=False)),
          file=ccfile)

    template = """
void {}({} *object, GDBusMethodInvocation *invocation{})
{{
    REQUIRE({}::singleton != nullptr);
    REQUIRE(object == {}::proxy_pointer());
    return {}::singleton->check_next<{}::{}>(object, invocation{});
}}
"""
    complete_fn_args = _mk_argument_list(method, True,
                                         _map_simple_type_to_ctype,
                                         need_return_types=True,
                                         need_prefixed_names=False)
    complete_forward_args = _mk_call_parameter_list(method, True,
                                                    need_return_types=True,
                                                    need_prefixed_names=False)
    print(template.format(
            _method_name(fn_prefix,
                         'complete_' + _to_snake_case(method.attrib['name'])),
            iface_type,
            _format_string_list(complete_fn_args, 0,
                                leading_sep=', ', leading_indent=False),
            cpp_namespace, cpp_namespace, cpp_namespace, cpp_namespace,
            method.attrib['name'] + 'Complete',
            _format_string_list(complete_forward_args, 0,
                                leading_sep=', ', leading_indent=False)),
          file=ccfile)


def _write_impl_body(ccfile, iface_prefix, c_namespace, cpp_namespace, iface):
    template = """template <>
TDBus::Proxy<{}> &TDBus::get_singleton()
{{
    static auto proxy(TDBus::Proxy<{}>::make_proxy_for_testing(
            "{}",
            "{}",
            {}::PROXY_POINTER_PATTERN));
    return proxy;
}}

{}::Mock *{}::singleton = nullptr;"""
    iface_name = iface.attrib['name']
    iface_name_stripped = _remove_prefix(iface_name, iface_prefix)
    iface_type = c_namespace.replace('_', '') + iface_name_stripped
    dbus_name = 'unittests.' + iface_name
    print(template.format(
            iface_type, iface_type,
            dbus_name, '/' + dbus_name.replace('.', '/'),
            cpp_namespace, cpp_namespace, cpp_namespace),
          file=ccfile)

    fn_prefix = c_namespace + '_' + _to_snake_case(iface_name_stripped)
    for method in iface.findall('method'):
        _write_method_call_mocks(ccfile, iface_name, iface_type, cpp_namespace,
                                 fn_prefix, method)


def main():
    parser = argparse.ArgumentParser(
        description='Generate C++ headers from D-Bus introspection data')
    parser.add_argument(
        '--interface', metavar='NAME', type=str, required=True,
        help='the D-Bus interface to generate the mock for')
    parser.add_argument(
        '--interface-prefix', metavar='PREFIX', type=str,
        help='string to strip from D-Bus interface names')
    parser.add_argument(
        '--c-namespace', metavar='NAMESPACE', type=str,
        help='the namespace used by the C code generated by gdbus-codegen')
    parser.add_argument(
        '--cpp-namespace', metavar='NAMESPACE', type=str, required=True,
        help='the namespace used by the generated mock')
    parser.add_argument(
        '--pointer-pattern', metavar='PREFIX', type=str, required=True,
        help='recognizable dummy value to use for D-Bus proxy pointers')
    parser.add_argument(
        '--output-hh', '-o', metavar='FILE', type=Path,
        help='write C++ header to this file instead of stdout')
    parser.add_argument(
        '--output-cc', '-O', metavar='FILE', type=Path,
        help='write C++ implementation to this file instead of stdout')
    parser.add_argument(
        '--include-guard', metavar='NAME', type=str,
        help='name of the #include guard written to the header file')
    parser.add_argument(
        'FILE', type=Path,
        help='XML file containing the D-Bus interface specification')
    args = parser.parse_args()
    options = vars(args)

    xmlfile = ET.parse(options['FILE'].open())
    interface_spec = xmlfile.findall('./interface[@name=\'' +
                                     options['interface'] + '\']')
    if len(interface_spec) == 1:
        interface_spec = interface_spec[0]
    else:
        print('Interface "{}" {} in {}'.format(
            options['interface'],
            'not found' if len(interface_spec) == 0 else 'is ambiguous',
            options['FILE']))
        sys.exit(10)

    hhfile = options['output_hh'].open('w') \
        if options['output_hh'] else sys.stdout
    ccfile = options['output_cc'].open('w') \
        if options['output_cc'] else sys.stdout

    include_guard = _mk_include_guard(options)
    mocked_header = options['FILE'].stem + '.hh'

    _write_header_top(hhfile, include_guard, mocked_header,
                      options['cpp_namespace'])
    _write_header_body(
        hhfile, options['interface_prefix'], options['c_namespace'],
        options['cpp_namespace'], options['pointer_pattern'], interface_spec)
    _write_header_bottom(hhfile, include_guard)

    mock_header_name = options['output_hh'].name \
        if options['output_hh'] else ''
    _write_impl_top(ccfile, mock_header_name)
    _write_impl_body(
        ccfile, options['interface_prefix'], options['c_namespace'],
        options['cpp_namespace'], interface_spec)


if __name__ == '__main__':
    main()
