/*
 * Copyright (C) 2015, 2016, 2017  T+A elektroakustik GmbH & Co. KG
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

#ifndef DE_TAHIFI_LISTS_ERRORS_H
#define DE_TAHIFI_LISTS_ERRORS_H

#ifndef DE_TAHIFI_LISTS_ERRORS_ENUM_NAME
#define DE_TAHIFI_LISTS_ERRORS_ENUM_NAME        DBusListsErrorCode
#endif /* !DE_TAHIFI_LISTS_ERRORS_ENUM_NAME */

#ifndef DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE
#define DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(V)    LIST_ERROR_ ## V
#endif /* !DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE */

enum DE_TAHIFI_LISTS_ERRORS_ENUM_NAME
{
    /*! No error occurred. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(OK) = 0U,

    /*! An internal error occurred (a bug). */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(INTERNAL),

    /*! Interrupted by user. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(INTERRUPTED),

    /*! The ID passed into the D-Bus method was invalid. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(INVALID_ID),

    /*! I/O error on physical medium (e.g., read error on some USB drive). */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(PHYSICAL_MEDIA_IO),

    /*! I/O error on the network (e.g., broken network connection). */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(NET_IO),

    /*! Network protocol error. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(PROTOCOL),

    /*! Authentication with some external system has failed. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(AUTHENTICATION),

    /*! The list is inconsistent and cannot be used. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(INCONSISTENT),

    /*! Operation not supported. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(NOT_SUPPORTED),

    /*! Operation not allowed. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(PERMISSION_DENIED),

    /*! The URI passed into the D-Bus method was invalid. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(INVALID_URI),

    /*! System is busy, try again later after waiting for at least 500 ms. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(BUSY_500),

    /*! System is busy, try again later after waiting for at least 1000 ms. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(BUSY_1000),

    /*! System is busy, try again later after waiting for at least 1500 ms. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(BUSY_1500),

    /*! System is busy, try again later after waiting for at least 3000 ms. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(BUSY_3000),

    /*! System is busy, try again later after waiting for at least 5000 ms. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(BUSY_5000),

    /*! System is busy, try again later at any point. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(BUSY),

    /*! Value out of range. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(OUT_OF_RANGE),

    /*! Some entity was empty when it wasn't supposed to. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(EMPTY),

    /*! Some overflow occurred (integer, buffer, ...). */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(OVERFLOWN),

    /*! Some underflow occurred (integer, buffer, ...). */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(UNDERFLOWN),

    /*! Stream URL invalid. Added to be more specific than INVALID_URI. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(INVALID_STREAM_URL),

    /*! StrBo URL invalid. Added to be more specific than INVALID_URI. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(INVALID_STRBO_URL),

    /*! Resource is not available. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(NOT_FOUND),

    /*! Stable name for the highest-valued error code. */
    DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(LAST_ERROR_CODE) = DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE(NOT_FOUND),
};

#undef DE_TAHIFI_LISTS_ERRORS_ENUM_NAME
#undef DE_TAHIFI_LISTS_ERRORS_ENUM_VALUE

#endif /* !DE_TAHIFI_LISTS_ERRORS_H */
