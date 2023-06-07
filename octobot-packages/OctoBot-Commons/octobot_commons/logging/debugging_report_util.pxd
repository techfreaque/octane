# cython: language_level=3
#  Drakkar-Software OctoBot-Commons
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.

cdef class DebuggingReporter:
    # cpdef void add_to_debugging_report(self, str key_to_set, str error_description, str additional_message, ? error, ? method)
    cdef void _add_to_debugging_report(self, str key_to_set, str message)
    cpdef void create_debugging_report(self)
    cdef void _finalize_debugging_report(self, str report)
    cpdef str debugging_report_main_template(self, str report)
