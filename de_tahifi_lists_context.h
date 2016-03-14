/*
 * Copyright (C) 2016  T+A elektroakustik GmbH & Co. KG
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

#ifndef DE_TAHIFI_LISTS_CONTEXT_H
#define DE_TAHIFI_LISTS_CONTEXT_H

#define DBUS_LISTS_CONTEXT_ID_BITS      4U
#define DBUS_LISTS_CONTEXT_ID_SHIFT     (32U - DBUS_LISTS_CONTEXT_ID_BITS)
#define DBUS_LISTS_CONTEXT_ID_MASK \
    (DBUS_LISTS_CONTEXT_ID_MAX << DBUS_LISTS_CONTEXT_ID_SHIFT)

#define DBUS_LISTS_CONTEXT_ID_MIN     0U
#define DBUS_LISTS_CONTEXT_ID_MAX     ((1U << DBUS_LISTS_CONTEXT_ID_BITS) - 1U)

#define DBUS_LISTS_CONTEXT_GET(ID) \
    (((ID) & DBUS_LISTS_CONTEXT_ID_MASK) >> DBUS_LISTS_CONTEXT_ID_SHIFT)

#endif /* !DE_TAHIFI_LISTS_CONTEXT_H */
