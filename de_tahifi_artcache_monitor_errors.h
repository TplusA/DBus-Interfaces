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

#ifndef DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_H
#define DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_H

#ifndef DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_NAME
#define DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_NAME  DBusArtCacheMonitorError
#endif /* DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_NAME */

#ifndef DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE
#define DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE(V)  AC_MONITOR_ERROR_ ## V
#endif /* DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE */

enum DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_NAME
{
    DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE(INTERNAL),
    DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE(DOWNLOAD_ERROR),
    DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE(FORMAT_NOT_SUPPORTED),
    DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE(OUT_OF_MEMORY),
    DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE(NO_SPACE_ON_DISK),
    DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE(IO_FAILURE),
    DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE(LAST_ERROR_CODE) = DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE(IO_FAILURE),
};

#undef DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_NAME
#undef DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_ENUM_VALUE

#endif /* !DE_TAHIFI_ARTCACHE_MONITOR_ERRORS_H */
