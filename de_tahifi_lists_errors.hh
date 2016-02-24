/*
 * Copyright (C) 2015, 2016  T+A elektroakustik GmbH & Co. KG
 *
 * This file is part of T+A Streaming Board D-Bus interfaces (T+A-D-Bus).
 *
 * T+A-D-Bus is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License, version 3 as
 * published by the Free Software Foundation.
 *
 * T+A-D-Bus is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with T+A-D-Bus.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef DE_TAHIFI_LISTS_ERRORS_HH
#define DE_TAHIFI_LISTS_ERRORS_HH

#include <inttypes.h>

class ListError
{
  public:
#ifndef DE_TAHIFI_LISTS_ERRORS_ENUM_NAME
#define DE_TAHIFI_LISTS_ERRORS_ENUM_NAME        Code
#endif /* !DE_TAHIFI_LISTS_ERRORS_ENUM_NAME */
#ifndef DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE
#define DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(V)    V
#endif /* !DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE */
#include "de_tahifi_lists_errors.h"

  private:
    /*!
     * String representations of the error codes.
     *
     * \attention
     *     This array must be sorted according to the values in the
     *     #ListError::Code enum and it must match its size.
     *
     * \attention
     *     This array must be explicitly instantiated in some C++ file,
     *     otherwise the linker will bail out with an error. Copy the
     *     following definition to some implementation file so that the linker
     *     can take it from there:
     *     \code constexpr const char *ListError::names_[]; \endcode
     */
    static constexpr const char *names_[] =
    {
        "OK",
        "INTERNAL",
        "INTERRUPTED",
        "INVALID_ID",
        "PHYSICAL_MEDIA_IO",
        "NET_IO",
        "PROTOCOL",
        "AUTHENTICATION",
        "INCONSISTENT",
        "NOT_SUPPORTED",
        "PERMISSION_DENIED",
    };

    static_assert(sizeof(names_) / sizeof(names_[0]) == static_cast<size_t>(ListError::Code::LAST_ERROR_CODE) + 1U,
                  "Mismatch between error codes enum and error strings");

    Code error_code_;

  public:
    constexpr explicit ListError(Code error_code = Code::OK) throw():
        error_code_(error_code)
    {}

    constexpr explicit ListError(unsigned int error_code) throw():
        error_code_(raw_to_code(error_code))
    {}

    constexpr Code get() const noexcept
    {
        return error_code_;
    }

    constexpr uint8_t get_raw_code() const noexcept { return uint8_t(error_code_); }

    ListError &operator=(Code code) noexcept
    {
        error_code_ = code;
        return *this;
    }

    constexpr bool operator==(Code code) const noexcept
    {
        return error_code_ == code;
    }

    constexpr bool operator!=(Code code) const noexcept
    {
        return !(*this == code);
    }

    constexpr bool operator==(const ListError &other) const noexcept
    {
        return *this == other.error_code_;
    }

    constexpr bool failed() const noexcept
    {
        return *this != Code::OK;
    }

    constexpr static Code raw_to_code(unsigned int raw_error_code)
    {
        return (raw_error_code <= Code::LAST_ERROR_CODE)
            ? Code(raw_error_code)
            : Code::INTERNAL;
    }

    constexpr static const char *code_to_string(Code error)
    {
        return error < sizeof(names_) / sizeof(names_[0])
            ? names_[error]
            : "***Invalid ListError code***";
    }

    constexpr const char *to_string() const
    {
        return ListError::code_to_string(error_code_);
    }
};

template <typename T>
static T& operator<<(T& os, const ::ListError &error)
{
    os << "ListError::Code::" << error.to_string();
    return os;
}

#endif /* !DE_TAHIFI_LISTS_ERRORS_HH */
