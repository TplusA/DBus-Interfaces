/*
 * Copyright (C) 2016, 2019  T+A elektroakustik GmbH & Co. KG
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
