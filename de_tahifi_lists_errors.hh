/*
 * Copyright (C) 2015  T+A elektroakustik GmbH & Co. KG
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
#define DE_TAHIFI_LISTS_ERRORS_ENUM_NAME        Code
#define DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(V)    V
#include "de_tahifi_lists_errors.h"

  private:
    Code error_code_;

  public:
    constexpr explicit ListError(Code error_code = Code::OK) throw():
        error_code_(error_code)
    {}

    uint8_t get_raw_code() const noexcept { return uint8_t(error_code_); }

    ListError &operator=(Code code) noexcept
    {
        error_code_ = code;
        return *this;
    }

    bool operator==(Code code) const noexcept
    {
        return error_code_ == code;
    }

    bool operator!=(Code code) const noexcept
    {
        return !(*this == code);
    }

    bool operator==(const ListError &other) const noexcept
    {
        return *this == other.error_code_;
    }

    bool failed() const noexcept
    {
        return *this != Code::OK;
    }

    static Code raw_to_code(unsigned int raw_error_code)
    {
        if(raw_error_code <= Code::LAST_ERROR_CODE)
            return Code(raw_error_code);
        else
            return Code::INTERNAL;
    }
};

template <typename T>
static T& operator<<(T& os, const ::ListError &error)
{
    /* must be sorted according to #ListError::Code enum */
    static constexpr const char *names[] =
    {
        "OK",
        "INTERNAL",
        "INVALID_ID",
        "PHYSICAL_MEDIA_IO",
        "NET_IO",
        "PROTOCOL",
        "AUTHENTICATION",
    };

    static constexpr char prefix[] = "ListError::Code::";

    if(error.get_raw_code() < sizeof(names) / sizeof(names[0]))
        os << prefix << names[error.get_raw_code()];
    else
        os << "***Invalid ListError code***";

    return os;
}

#endif /* !DE_TAHIFI_LISTS_ERRORS_HH */
