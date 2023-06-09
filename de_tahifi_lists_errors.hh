/*
 * Copyright (C) 2015, 2016, 2017, 2019, 2022  T+A elektroakustik GmbH & Co. KG
 *
 * This file is part of T+A Streaming Board D-Bus interfaces (T+A-D-Bus).
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA  02110-1301, USA.
 */

#ifndef DE_TAHIFI_LISTS_ERRORS_HH
#define DE_TAHIFI_LISTS_ERRORS_HH

#include <cinttypes>

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
        "INVALID_URI",
        "BUSY_500",
        "BUSY_1000",
        "BUSY_1500",
        "BUSY_3000",
        "BUSY_5000",
        "BUSY",
        "OUT_OF_RANGE",
        "EMPTY",
        "OVERFLOWN",
        "UNDERFLOWN",
        "INVALID_STREAM_URL",
        "INVALID_STRBO_URL",
        "NOT_FOUND",
    };

    static_assert(sizeof(names_) / sizeof(names_[0]) == static_cast<std::size_t>(ListError::Code::LAST_ERROR_CODE) + 1U,
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

    constexpr bool busy() const noexcept
    {
        switch(error_code_)
        {
          case Code::BUSY:
          case Code::BUSY_500:
          case Code::BUSY_1000:
          case Code::BUSY_1500:
          case Code::BUSY_3000:
          case Code::BUSY_5000:
            return true;

          case Code::OK:
          case Code::INTERNAL:
          case Code::INTERRUPTED:
          case Code::INVALID_ID:
          case Code::PHYSICAL_MEDIA_IO:
          case Code::NET_IO:
          case Code::PROTOCOL:
          case Code::AUTHENTICATION:
          case Code::INCONSISTENT:
          case Code::NOT_SUPPORTED:
          case Code::PERMISSION_DENIED:
          case Code::INVALID_URI:
          case Code::OUT_OF_RANGE:
          case Code::EMPTY:
          case Code::OVERFLOWN:
          case Code::UNDERFLOWN:
          case Code::INVALID_STREAM_URL:
          case Code::INVALID_STRBO_URL:
          case Code::NOT_FOUND:
            break;
        }

        return false;
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
