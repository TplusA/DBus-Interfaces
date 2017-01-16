#! /usr/bin/env python

#
# Copyright (C) 2015  T+A elektroakustik GmbH & Co. KG
#
# This file is part of T+A-D-Bus.
#
# T+A-D-Bus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 3 as
# published by the Free Software Foundation.
#
# T+A-D-Bus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with T+A-D-Bus.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import print_function

import sys
import getopt
import re
import xml.dom.minidom

def error_exit(error_message, exit_code = 1):
    print("Error: " + error_message, file = sys.stderr)
    sys.exit(exit_code)

class CommentedElement:
    def __init__(self, node, comment):
        self.node = node
        self.comment_lines = CommentedElement.format_comment(comment)

    def get_comment(self, prefix = ""):
        return "\n".join(map(lambda x: (prefix + x).rstrip(), self.comment_lines))

    @staticmethod
    def format_comment(comment):
        if not comment:
            return None

        lines = comment.split("\n")
        indentation = 80

        for line in lines:
            stripped_len = len(line.lstrip())
            if stripped_len > 0:
                indentation = min(len(line) - stripped_len, indentation)

        empty_lines = 0
        dest_lines = []

        for i in range(len(lines)):
            temp = lines[i][indentation : ]

            if len(temp.lstrip()) == 0:
                empty_lines += 1
            else:
                if empty_lines and len(dest_lines) > 0:
                    dest_lines.append("")

                dest_lines.append(temp)
                empty_lines = 0

        return dest_lines

def get_elements_with_comments(nodes):
    elements = []
    current_comment = None

    for n in nodes:
        if n.nodeType == xml.dom.minidom.Node.TEXT_NODE:
            continue

        if n.nodeType == xml.dom.minidom.Node.COMMENT_NODE:
            current_comment = n.data
        else:
            elements.append(CommentedElement(n, current_comment))
            current_comment = None

    return elements

def concat_c_names(first, second):
    return first + "_" + camel_case_to_c_style(second)

def camel_case_to_c_style(cc):
    return re.sub(r"([^A-Z_])([A-Z])", r"\1_\2", cc).lower()

def ifacename_to_cstyle(iface_name):
    return camel_case_to_c_style(iface_name.replace(".", "_"))

def ifacename_to_refname(kind, iface_name):
    return "dbus_" + kind + "_" + ifacename_to_cstyle(iface_name)

def write_section(section_name, verb, iface_name, f):
    print("\n\\section " + ifacename_to_refname(section_name.lower(), iface_name) + " " + section_name, file = f)
    print("\nHere is a list of " + section_name.lower() + " " + verb + " by the <tt>" + iface_name + "</tt> interface:\n", file = f)

def get_partial_name_for_c_function(name, accept_all_names):
    if accept_all_names or name.lower() != "type":
        return name
    else:
        return name + "_"

def write_table(kind, prefix, suffix, members, accept_all_names, mdfile):
    table_rows = [[kind + " name", "Related function"]]

    for m in members:
        name = m.node.getAttribute("name")
        name_in_fn = get_partial_name_for_c_function(name, accept_all_names)
        fnname = concat_c_names(prefix, name_in_fn)

        if suffix:
            fnname = concat_c_names(fnname, suffix)

        table_rows.append(["<tt>" + name + "</tt>", "#" + fnname + "()"])

    col1_width = 0
    col2_width = 0
    for row in table_rows:
        col1_width = max(len(row[0]), col1_width)
        col2_width = max(len(row[1]), col2_width)

    format_string = "{:<" + str(col1_width) + "} | {:}"

    row = table_rows.pop(0)
    print(format_string.format(row[0], row[1]), file = mdfile)
    print("-" * (col1_width + 1) + "|" + "-" * (col2_width + 1), file = mdfile)

    for row in table_rows:
        print(format_string.format(row[0], row[1]), file = mdfile)

dbus_type_to_ctype = {
    "b": "gboolean",
    "d": "gdouble",
    "i": "gint",
    "n": "gint16",
    "q": "guint16",
    "u": "guint",
    "x": "gint64",
    "t": "guint64",
    "y": "guchar",
    "v": "GVariant *"
}

dbus_input_type_to_ctype = {
    "s": "const gchar *",
}

dbus_output_type_to_ctype = {
    "s": "gchar *",
    "as": "gchar **",
}

dbus_signal_type_to_ctype = {
    "s": "const gchar *",
}

dbus_property_type_to_ctype = {
    "as": "const gchar *const *"
}

def generate_specific_parameter_list(parameters, args, prefix, required_direction = None, is_signal = False):
    if required_direction == "in":
        direction_specific_dbus_type_to_ctype = dbus_input_type_to_ctype
    elif is_signal:
        direction_specific_dbus_type_to_ctype = dbus_signal_type_to_ctype
    elif required_direction == "out":
        direction_specific_dbus_type_to_ctype = dbus_output_type_to_ctype
    else:
        direction_specific_dbus_type_to_ctype = None

    for arg in args:
        name = arg.getAttribute("name")
        dbus_type = arg.getAttribute("type")
        direction = arg.getAttribute("direction")

        if required_direction != None:
            if not direction:
                error_exit("No direction specified for argument " + name)

            if direction != required_direction:
                continue

        if dbus_type in dbus_type_to_ctype:
            c_type = dbus_type_to_ctype[dbus_type]
        elif direction_specific_dbus_type_to_ctype and dbus_type in direction_specific_dbus_type_to_ctype:
            c_type = direction_specific_dbus_type_to_ctype[dbus_type]
        elif len(dbus_type) > 1:
            c_type = "GVariant *"
        else:
            error_exit('Unsupported D-Bus type "' + dbus_type + '" used for argument "' + name + '"')

        parameters.append(c_type + " " + concat_c_names(prefix, name))

def generate_specific_parameter_list_for_property(parameters, prop):
    name = prop.getAttribute("name")
    dbus_type = prop.getAttribute("type")

    if dbus_type in dbus_type_to_ctype:
        c_type = dbus_type_to_ctype[dbus_type]
    elif dbus_input_type_to_ctype and dbus_type in dbus_input_type_to_ctype:
        c_type = dbus_input_type_to_ctype[dbus_type]
    elif dbus_type in dbus_property_type_to_ctype:
        c_type = dbus_property_type_to_ctype[dbus_type]
    elif len(dbus_type) > 1:
        c_type = "GVariant *"
    else:
        error_exit('Unsupported D-Bus type "' + dbus_type + '" used for property "' + name + '"')

    parameters.append(c_type + " value")


def generate_signal_emit_parameter_list(proxy_typename, arguments):
    args = arguments.getElementsByTagName("arg")

    parameters = []
    parameters.append(proxy_typename + " *object")
    generate_specific_parameter_list(parameters, args, "arg", is_signal = True)

    return ", ".join(parameters)

def generate_method_call_parameter_list(proxy_typename, arguments):
    args = arguments.getElementsByTagName("arg")

    parameters = []
    parameters.append(proxy_typename + " *proxy")
    generate_specific_parameter_list(parameters, args, "arg", "in")
    generate_specific_parameter_list(parameters, args, "*out", "out")
    parameters.append("GCancellable *cancellable")
    parameters.append("GError **error")

    return ", ".join(parameters)

def generate_property_set_parameter_list(proxy_typename, arguments):
    parameters = []
    parameters.append(proxy_typename + " *object")
    generate_specific_parameter_list_for_property(parameters, arguments)

    return ", ".join(parameters)

def generate_proxy_typename(c_namespace, iface_name):
    return re.sub(r"_", r"", c_namespace) + iface_name;

def write_documentation(c_namespace, rettype, prefix, suffix, proxy_typename, generate_parameter_list, members, accept_all_names, hfile):
    for m in members:
        if not m.comment_lines:
            continue

        print(r"/*!", file = hfile)

        name = m.node.getAttribute("name")
        name_in_fn = get_partial_name_for_c_function(name, accept_all_names)
        fnname = concat_c_names(prefix, name_in_fn)

        if suffix:
            see_also = fnname
            fnname = concat_c_names(see_also, suffix)
        else:
            see_also = None

        print(r" * \fn " + rettype + " " + fnname + "(" + generate_parameter_list(proxy_typename, m.node) + ")", file = hfile)
        print(r" *", file = hfile)

        print(m.get_comment(r" * "), file = hfile)

        if see_also:
            print(" *\n * \\see #" + see_also + "()", file = hfile)

        print(r" */", file = hfile)

def strip_prefix_from_interface_name(iface_name, strip_prefix):
    if iface_name.startswith(strip_prefix):
        iface_name = iface_name[len(strip_prefix) : ]

    return iface_name

def generate_files_from_interfaces(interfaces, component_name, c_namespace, strip_prefix, hfile, mdfile,
                                   exclude_signals, exclude_methods, exclude_properties):
    print(r"""\page dbus_interfaces D-Bus interface documentation

Interfaces of _""" + component_name + "_:", file = mdfile)

    signal_tag_name =   "signal"
    method_tag_name =   "method"
    property_tag_name = "property"
    if exclude_signals:    signal_tag_name = None
    if exclude_methods:    method_tag_name = None
    if exclude_properties: property_tag_name = None

    for iface in interfaces:
        print(r"- \subpage " + ifacename_to_refname("iface", iface.node.getAttribute("name")), file = mdfile)

    for iface in interfaces:
        if iface.node.nodeType != xml.dom.minidom.Node.ELEMENT_NODE:
            error_exit("Unexpected node type " + str(iface.nodeType))

        if iface.node.tagName != "interface":
            error_exit('Unexpected tag "' + iface.node.tagName + '", expected interface')

        members = get_elements_with_comments(iface.node.childNodes)
        all_signals = [m for m in members if m.node.tagName == signal_tag_name]
        all_methods = [m for m in members if m.node.tagName == method_tag_name]
        all_properties = [m for m in members if m.node.tagName == property_tag_name]

        iface_name = iface.node.getAttribute("name")
        fnname_prefix = ifacename_to_cstyle(strip_prefix_from_interface_name(iface_name, strip_prefix))
        if c_namespace:
            fnname_prefix = c_namespace + "_" + fnname_prefix

        print("\n\n\\page " + ifacename_to_refname("iface", iface_name) + " Interface " + iface_name, file = mdfile)

        if iface.comment_lines:
            print("\n" + iface.get_comment(), file = mdfile)

        if len(all_signals) == 0 and len(all_methods) == 0 and len(all_properties) == 0:
            print("\nThis interface is not used by this software.", file = mdfile)
            continue

        proxy_typename = generate_proxy_typename(c_namespace, strip_prefix_from_interface_name(iface_name, strip_prefix))

        if len(all_signals) > 0:
            write_section("Signals", "emitted", iface_name, mdfile)
            write_table("Signal", fnname_prefix + "_emit", None, all_signals, True, mdfile)
            write_documentation(c_namespace, "void", fnname_prefix + "_emit", None, proxy_typename, generate_signal_emit_parameter_list, all_signals, True, hfile)

        if len(all_methods) > 0:
            write_section("Methods", "implemented", iface_name, mdfile)
            write_table("Method", fnname_prefix + "_call", "sync", all_methods, True, mdfile)
            write_documentation(c_namespace, "gboolean", fnname_prefix + "_call", "sync", proxy_typename, generate_method_call_parameter_list, all_methods, True, hfile)

        if len(all_properties) > 0:
            write_section("Properties", "exposed", iface_name, mdfile)
            write_table("Property", fnname_prefix + "_set", None, all_properties, False, mdfile)
            write_documentation(c_namespace, "void", fnname_prefix + "_set", None, proxy_typename, generate_property_set_parameter_list, all_properties, False, hfile)


def usage(exit_code = 1):
    print(r"""\
Usage: """ + sys.argv[0] + r""" -i xmlfile -H hfile -o mdfile -n name [-c ns] [-s strip] [-h]

Options:
-i file  Input XML file containing D-Bus introspection data.
-H file  Output header file for Doxygen containing only comments for functions
         supposedly generated by gdbus-codegen. The comments, if any, are
         extracted from the introspection XML file.
-o file  Output Markdown file for Doxygen containing the documentation pages
         for D-Bus interfaces defined in the introspection XML file.
-n str   Name of the software component as it should appear in the
         documentation.
-c str   C namespace prefix for generated C names.
-s str   Prefix to remove from the interface names for generated C names.
-x str   Exclude D-Bus signals, methods, or properties from output (by default,
         all parts of the defined D-Bus interface are extracted). The str may
         be one of "signals", "methods", or "properties". This option may be
         specified multiple times for cumulative effect.
-h       This help screen.""", file = sys.stderr)
    sys.exit(exit_code)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:i:hH:n:o:s:x:")
    except getopt.GetoptError as err:
        error_exit(str(err))

    xml_input_file = None
    doxygen_markdown_file = None
    doxygen_header_file = None
    component_name = None
    c_namespace = ""
    strip_from_interface_name = ""
    exclude_signals = False
    exclude_methods = False
    exclude_properties = False

    for o, a in opts:
        if o == "-h":   usage(0)
        elif o == '-c': c_namespace = a
        elif o == "-i": xml_input_file = a
        elif o == "-H": doxygen_header_file = a
        elif o == '-n': component_name = a
        elif o == "-o": doxygen_markdown_file = a
        elif o == '-s': strip_from_interface_name = a
        elif o == '-x':
            if a == 'signals':      exclude_signals = True
            elif a == 'methods':    exclude_methods = True
            elif a == 'properties': exclude_properties = True
            else:                   usage()

    if not xml_input_file or not doxygen_header_file or not doxygen_markdown_file or not component_name:
        usage()

    xmldoc = xml.dom.minidom.parse(xml_input_file)

    node_def = xmldoc.getElementsByTagName("node")
    if len(node_def) != 1:
        error_exit("Found " + str(len(node_def)) + " node elements.")

    interfaces = get_elements_with_comments(node_def[0].childNodes)
    if len(interfaces) < 1:
        error_exit("No interfaces defined in " + xml_input_file)

    with open(doxygen_header_file, "w+") as hfile, open(doxygen_markdown_file, "w+") as mdfile:
        generate_files_from_interfaces(interfaces, component_name, c_namespace,
                                       strip_from_interface_name, hfile, mdfile,
                                       exclude_signals, exclude_methods, exclude_properties)

if __name__ == "__main__":
    main()
