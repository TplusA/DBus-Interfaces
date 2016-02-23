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

#ifndef DE_TAHIFI_LISTS_ITEM_KINDS_H
#define DE_TAHIFI_LISTS_ITEM_KINDS_H

#ifndef DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_NAME
#define DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_NAME        DBusListsItemKind
#endif /* !DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_NAME */

#ifndef DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE
#define DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(V)    LIST_ITEM_KIND_ ## V
#endif /* !DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE */

enum DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_NAME
{
    /*! Plain string, could be file, could be device node, or anything. */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(OPAQUE) = 0U,

    /*! Something that cannot be read. */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(LOCKED),

    /*! Maybe a stream. */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(REGULAR_FILE),

    /*! A directory. */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(DIRECTORY),

    /*! Search form that requires parameters when getting ID. */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(SEARCH_FORM),
};

#undef DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_NAME
#undef DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE

#endif /* !DE_TAHIFI_LISTS_ITEM_KINDS_H */
