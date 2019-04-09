/*
 * Copyright (C) 2017, 2019  T+A elektroakustik GmbH & Co. KG
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

#ifndef DE_TAHIFI_ARTCACHE_ERRORS_HH
#define DE_TAHIFI_ARTCACHE_ERRORS_HH

namespace ArtCache
{

class ReadError
{
  public:
#ifndef DE_TAHIFI_ARTCACHE_READ_ERRORS_ENUM_NAME
#define DE_TAHIFI_ARTCACHE_READ_ERRORS_ENUM_NAME        Code
#endif /* !DE_TAHIFI_ARTCACHE_READ_ERRORS_ENUM_NAME */
#ifndef DE_TAHIFI_ARTCACHE_READ_ERRORS_ENUM_VALUE
#define DE_TAHIFI_ARTCACHE_READ_ERRORS_ENUM_VALUE(V)    V
#endif /* !DE_TAHIFI_ARTCACHE_READ_ERRORS_ENUM_VALUE */
#include "de_tahifi_artcache_read_errors.h"

  private:
    /*!
     * String representations of the error codes.
     *
     * \attention
     *     This array must be sorted according to the values in the
     *     #ArtCache::ReadError::Code enum and it must match its size.
     *
     * \attention
     *     This array must be explicitly instantiated in some C++ file,
     *     otherwise the linker will bail out with an error. Copy the
     *     following definition to some implementation file so that the linker
     *     can take it from there:
     *     \code constexpr const char *ArtCache::ReadError::names_[]; \endcode
     */
    static constexpr const char *names_[] =
    {
        "OK",
        "UNCACHED",
        "KEY_UNKNOWN",
        "BUSY",
        "FORMAT_NOT_SUPPORTED",
        "IO_FAILURE",
        "INTERNAL",
    };

    static_assert(sizeof(names_) / sizeof(names_[0]) == static_cast<size_t>(ReadError::Code::LAST_ERROR_CODE) + 1U,
                  "Mismatch between error codes enum and error strings");

    Code error_code_;

  public:
    constexpr explicit ReadError(Code error_code = Code::OK) throw():
        error_code_(error_code)
    {}

    constexpr explicit ReadError(unsigned int error_code) throw():
        error_code_(raw_to_code(error_code))
    {}

    constexpr Code get() const noexcept
    {
        return error_code_;
    }

    constexpr uint8_t get_raw_code() const noexcept { return uint8_t(error_code_); }

    ReadError &operator=(Code code) noexcept
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

    constexpr bool operator==(const ReadError &other) const noexcept
    {
        return *this == other.error_code_;
    }

    constexpr bool failed() const noexcept
    {
        return *this != Code::OK && *this != Code::UNCACHED;
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
            : "***Invalid ReadError code***";
    }

    constexpr const char *to_string() const
    {
        return ReadError::code_to_string(error_code_);
    }
};

class MonitorError
{
  public:
#ifndef DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_NAME
#define DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_NAME        Code
#endif /* !DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_NAME */
#ifndef DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE
#define DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE(V)    V
#endif /* !DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE */
#include "de_tahifi_artcache_monitor_errors.h"

  private:
    /*!
     * String representations of the error codes.
     *
     * \attention
     *     This array must be sorted according to the values in the
     *     #ArtCache::MonitorError::Code enum and it must match its size.
     *
     * \attention
     *     This array must be explicitly instantiated in some C++ file,
     *     otherwise the linker will bail out with an error. Copy the
     *     following definition to some implementation file so that the linker
     *     can take it from there:
     *     \code constexpr const char *ArtCache::MonitorError::names_[]; \endcode
     */
    static constexpr const char *names_[] =
    {
        "INTERNAL",
        "DOWNLOAD_ERROR",
        "FORMAT_NOT_SUPPORTED",
        "OUT_OF_MEMORY",
        "NO_SPACE_ON_DISK",
        "IO_FAILURE",
    };

    static_assert(sizeof(names_) / sizeof(names_[0]) == static_cast<size_t>(MonitorError::Code::LAST_ERROR_CODE) + 1U,
                  "Mismatch between error codes enum and error strings");

    Code error_code_;

  public:
    constexpr explicit MonitorError(Code error_code) throw():
        error_code_(error_code)
    {}

    constexpr explicit MonitorError(unsigned int error_code) throw():
        error_code_(raw_to_code(error_code))
    {}

    constexpr Code get() const noexcept
    {
        return error_code_;
    }

    constexpr uint8_t get_raw_code() const noexcept { return uint8_t(error_code_); }

    MonitorError &operator=(Code code) noexcept
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

    constexpr bool operator==(const MonitorError &other) const noexcept
    {
        return *this == other.error_code_;
    }

    constexpr bool failed() const noexcept
    {
        return true;
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
            : "***Invalid MonitorError code***";
    }

    constexpr const char *to_string() const
    {
        return MonitorError::code_to_string(error_code_);
    }
};

}

template <typename T>
static T& operator<<(T& os, const ::ArtCache::ReadError &error)
{
    os << "ArtCache::ReadError::Code::" << error.to_string();
    return os;
}

template <typename T>
static T& operator<<(T& os, const ::ArtCache::MonitorError &error)
{
    os << "ArtCache::MonitorError::Code::" << error.to_string();
    return os;
}

#endif /* !DE_TAHIFI_ARTCACHE_ERRORS_HH */
