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

#ifndef DE_TAHIFI_LISTS_ITEM_KINDS_HH
#define DE_TAHIFI_LISTS_ITEM_KINDS_HH

class ListItemKind
{
  public:
#ifndef DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_NAME
#define DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_NAME        Kind
#endif /* !DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_NAME */
#ifndef DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE
#define DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE(V)    V
#endif /* !DE_TAHIFI_LISTS_ITEM_KINDS_ENUM_VALUE */
#include "de_tahifi_lists_item_kinds.h"

  private:
    /*!
     * The item kind as raw number.
     *
     * This value is stored as a uint8_t to conserve memory. The #ListItemKind
     * class ensures type-safety.
     */
    uint8_t kind_;

  public:
    constexpr explicit ListItemKind(Kind item_kind) throw():
        kind_(item_kind)
    {}

    constexpr Kind get() const noexcept { return Kind(kind_); }

    constexpr uint8_t get_raw_code() const noexcept { return kind_; }

    bool is_directory() const
    {
        switch(kind_)
        {
          case Kind::DIRECTORY:
            return true;

          case Kind::OPAQUE:
          case Kind::LOCKED:
          case Kind::REGULAR_FILE:
          case Kind::SEARCH_FORM:
            break;
        }

        return false;
    }
};

#endif /* !DE_TAHIFI_LISTS_ITEM_KINDS_HH */
