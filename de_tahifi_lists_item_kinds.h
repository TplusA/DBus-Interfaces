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

    /*!
     * Something that cannot be read.
     *
     * \todo It is incorrect to treat \c LOCKED as a kind of its own. It must
     *       be a flag that can be combined with other kinds. E.g., it should
     *       be possible to have a locked file, a locked directory, a locked
     *       server, or a locked playlist directory.
     */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(LOCKED),

    /*! Maybe a stream. */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(REGULAR_FILE),

    /*! A directory. */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(DIRECTORY),

    /*! A server (treated as special kind of directory). */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(SERVER),

    /*! A device (treated as special kind of directory). */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(STORAGE_DEVICE),

    /*! Search form that requires parameters when getting ID. */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(SEARCH_FORM),

    /*! A playlist stored on file. */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(PLAYLIST_FILE),

    /*! A playlist represented as directory structure. */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(PLAYLIST_DIRECTORY),

    /*! The list entry for logging out from an external service. */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(LOGOUT_LINK),

    /*! Stable name for the highest-valued item kind ID. */
    DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(LAST_ITEM_KIND) = DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(LOGOUT_LINK),
};

#undef DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_NAME
#undef DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE

#endif /* !DE_TAHIFI_LISTS_ITEM_KINDS_H */
