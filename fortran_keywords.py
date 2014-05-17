#!/usr/bin/env python
# KWRD1= """access blank direct exist file fmt form formatted iostat name named nextrec number opened rec recl sequential status unformatted
# unit alog alog10 amax0 amax1 amin0 amin1 amod cabs ccos cexp clog csin csqrt dabs dacos dasin datan datan2 dcos dcosh ddim dexp dint
# dlog dlog10 dmax1 dmin1 dmod dnint dsign dsin dsinh dsqrt dtan dtanh float iabs idim idint idnint ifix isign max0 max1 min0 min1
# sngl algama cdabs cdcos cdexp cdlog cdsin cdsqrt cqabs cqcos cqexp cqlog cqsin cqsqrt dcmplx dconjg derf derfc dfloat dgamma dimag
# dlgama iqint qabs qacos qasin qatan qatan2 qcmplx qconjg qcos qcosh qdim qerf qerfc qexp qgamma qimag qlgama qlog qlog10 qmax1 qmin1
# qmod qnint qsign qsin qsinh qsqrt qtan qtanh abs acos aimag aint anint asin atan atan2 char cmplx conjg cos cosh exp ichar index int
# log log10 max min nint sign sin sinh sqrt tan tanh dim lge lgt lle llt mod eq eqv neq assign pause goto go to len real implicit
# logical external format continue type none private public intent optional pointer target allocatable in out module use only contains
# result operator assignment interface recursive allocate deallocate nullify cycle exit select case default where elsewhere pad
# position action delim readwrite eor advance nml adjustl adjustr all allocated any associated bit_size btest ceiling count cshift
# date_and_time digits dot_product eoshift epsilon exponent floor fraction huge iand ibclr ibits ibset ieor ior ishft ishftc lbound
# len_trim matmul maxexponent maxloc maxval merge minexponent minloc minval modulo mvbits nearest pack precision present product radix
# random_number random_seed range repeat reshape rrspacing scale scan selected_int_kind selected_real_kind set_exponent shape size
# spacing spread sum system_clock tiny transpose trim ubound unpack verify not kind function interface module program subroutine do
# where procedure namelist while achar iachar transfer include sequence else if end endif enddo endselect double precision complex
# block data common equivalence data dble dprod forall null cpu_time elemental pure command_argument_count get_command
# get_command_argument get_environment_variable is_iostat_end is_iostat_eor move_alloc new_line selected_char_kind same_type_as
# extends_type_of c_null_char c_alert c_backspace c_form_feed c_new_line c_carriage_return c_horizontal_tab c_vertical_tab c_int
# c_short c_long c_long_long c_signed_char c_size_t c_int8_t c_int16_t c_int32_t c_int64_t c_int_least8_t c_int_least16_t
# c_int_least32_t c_int_least64_t c_int_fast8_t c_int_fast16_t c_int_fast32_t c_int_fast64_t c_intmax_t C_intptr_t c_float c_double
# c_long_double c_float_complex c_double_complex c_long_double_complex c_bool c_char c_null_ptr c_null_funptr iso_c_binding c_loc
# c_funloc c_associated  c_f_pointer c_f_procpointer c_ptr c_funptr iso_fortran_env character_storage_size error_unit
# file_storage_size input_unit iostat_end iostat_eor numeric_storage_size output_unit ieee_arithmetic ieee_support_underflow_control
# ieee_get_underflow_mode ieee_set_underflow_mode flush wait decimal round iomsg asynchronous nopass non_overridable pass protected
# volatile abstract extends import non_intrinsic value bind deferred generic final enumerator class associate enum acosh asinh atanh
# bessel_j0 bessel_j1 bessel_jn bessel_y0 bessel_y1 bessel_yn erf erfc erfc_scaled gamma log_gamma hypot norm2 atomic_define
# atomic_ref execute_command_line leadz trailz storage_size merge_bits bge bgt ble blt dshiftl dshiftr findloc iall iany iparity
# image_index lcobound ucobound maskl maskr num_images parity popcnt poppar shifta shiftl shiftr this_image newunit contiguous"""
# 
# def unique_list(l):
#     ulist = []
#     [ulist.append(x) for x in l if x not in ulist]
#     return ulist
# 
# 
# # KWRD2=unique_list(KWRD1.split())
# KWRD2=KWRD1.replace('\n', ' ').replace('\r', '').replace('  ', ' ').lower().split(' ')
# KWRD3=unique_list(KWRD2)
# KWRD3.sort()
# print(KWRD3)


FortranKeywords=['abs', 'abstract', 'access', 'achar', 'acos', 'acosh', 'action', 'adjustl', 'adjustr', 'advance', 'aimag', 'aint', 'algama', 'all', 'allocatable', 'allocate', 'allocated',
'alog', 'alog10', 'amax0', 'amax1', 'amin0', 'amin1', 'amod', 'anint', 'any', 'asin', 'asinh', 'assign', 'assignment', 'associate', 'associated', 'asynchronous', 'atan', 'atan2', 'atanh',
'atomic_define', 'atomic_ref', 'bessel_j0', 'bessel_j1', 'bessel_jn', 'bessel_y0', 'bessel_y1', 'bessel_yn', 'bge', 'bgt', 'bind', 'bit_size', 'blank', 'ble', 'block', 'blt', 'btest',
'c_alert', 'c_associated', 'c_backspace', 'c_bool', 'c_carriage_return', 'c_char', 'c_double', 'c_double_complex', 'c_f_pointer', 'c_f_procpointer', 'c_float', 'c_float_complex',
'c_form_feed', 'c_funloc', 'c_funptr', 'c_horizontal_tab', 'c_int', 'c_int16_t', 'c_int32_t', 'c_int64_t', 'c_int8_t', 'c_int_fast16_t', 'c_int_fast32_t', 'c_int_fast64_t',
'c_int_fast8_t', 'c_int_least16_t', 'c_int_least32_t', 'c_int_least64_t', 'c_int_least8_t', 'c_intmax_t', 'c_intptr_t', 'c_loc', 'c_long', 'c_long_double', 'c_long_double_complex',
'c_long_long', 'c_new_line', 'c_null_char', 'c_null_funptr', 'c_null_ptr', 'c_ptr', 'c_short', 'c_signed_char', 'c_size_t', 'c_vertical_tab', 'cabs', 'case', 'ccos', 'cdabs', 'cdcos',
'cdexp', 'cdlog', 'cdsin', 'cdsqrt', 'ceiling', 'cexp', 'char', 'character_storage_size', 'class', 'clog', 'cmplx', 'command_argument_count', 'common', 'complex', 'conjg', 'contains',
'contiguous', 'continue', 'cos', 'cosh', 'count', 'cpu_time', 'cqabs', 'cqcos', 'cqexp', 'cqlog', 'cqsin', 'cqsqrt', 'cshift', 'csin', 'csqrt', 'cycle', 'dabs', 'dacos', 'dasin', 'data',
'datan', 'datan2', 'date_and_time', 'dble', 'dcmplx', 'dconjg', 'dcos', 'dcosh', 'ddim', 'deallocate', 'decimal', 'default', 'deferred', 'delim', 'derf', 'derfc', 'dexp', 'dfloat',
'dgamma', 'digits', 'dim', 'dimag', 'dint', 'direct', 'dlgama', 'dlog', 'dlog10', 'dmax1', 'dmin1', 'dmod', 'dnint', 'do', 'dot_product', 'double', 'dprod', 'dshiftl', 'dshiftr', 'dsign',
'dsin', 'dsinh', 'dsqrt', 'dtan', 'dtanh', 'elemental', 'else', 'elsewhere', 'end', 'enddo', 'endif', 'endselect', 'enum', 'enumerator', 'eor', 'eoshift', 'epsilon', 'eq', 'equivalence',
'eqv', 'erf', 'erfc', 'erfc_scaled', 'error_unit', 'execute_command_line', 'exist', 'exit', 'exp', 'exponent', 'extends', 'extends_type_of', 'external', 'file', 'file_storage_size',
'final', 'findloc', 'float', 'floor', 'flush', 'fmt', 'forall', 'form', 'format', 'formatted', 'fraction', 'function', 'gamma', 'generic', 'get_command', 'get_command_argument',
'get_environment_variable', 'go', 'goto', 'huge', 'hypot', 'iabs', 'iachar', 'iall', 'iand', 'iany', 'ibclr', 'ibits', 'ibset', 'ichar', 'idim', 'idint', 'idnint', 'ieee_arithmetic',
'ieee_get_underflow_mode', 'ieee_set_underflow_mode', 'ieee_support_underflow_control', 'ieor', 'if', 'ifix', 'image_index', 'implicit', 'import', 'in', 'include', 'index', 'input_unit',
'int', 'intent', 'interface', 'iomsg', 'ior', 'iostat', 'iostat_end', 'iostat_eor', 'iparity', 'iqint', 'is_iostat_end', 'is_iostat_eor', 'ishft', 'ishftc', 'isign', 'iso_c_binding',
'iso_fortran_env', 'kind', 'lbound', 'lcobound', 'leadz', 'len', 'len_trim', 'lge', 'lgt', 'lle', 'llt', 'log', 'log10', 'log_gamma', 'logical', 'maskl', 'maskr', 'matmul', 'max', 'max0',
'max1', 'maxexponent', 'maxloc', 'maxval', 'merge', 'merge_bits', 'min', 'min0', 'min1', 'minexponent', 'minloc', 'minval', 'mod', 'module', 'modulo', 'move_alloc', 'mvbits', 'name',
'named', 'namelist', 'nearest', 'neq', 'new_line', 'newunit', 'nextrec', 'nint', 'nml', 'non_intrinsic', 'non_overridable', 'none', 'nopass', 'norm2', 'not', 'null', 'nullify',
'num_images', 'number', 'numeric_storage_size', 'only', 'opened', 'operator', 'optional', 'out', 'output_unit', 'pack', 'pad', 'parity', 'pass', 'pause', 'pointer', 'popcnt', 'poppar',
'position', 'precision', 'present', 'private', 'procedure', 'product', 'program', 'protected', 'public', 'pure', 'qabs', 'qacos', 'qasin', 'qatan', 'qatan2', 'qcmplx', 'qconjg', 'qcos',
'qcosh', 'qdim', 'qerf', 'qerfc', 'qexp', 'qgamma', 'qimag', 'qlgama', 'qlog', 'qlog10', 'qmax1', 'qmin1', 'qmod', 'qnint', 'qsign', 'qsin', 'qsinh', 'qsqrt', 'qtan', 'qtanh', 'radix',
'random_number', 'random_seed', 'range', 'readwrite', 'real', 'rec', 'recl', 'recursive', 'repeat', 'reshape', 'result', 'round', 'rrspacing', 'same_type_as', 'scale', 'scan', 'select',
'selected_char_kind', 'selected_int_kind', 'selected_real_kind', 'sequence', 'sequential', 'set_exponent', 'shape', 'shifta', 'shiftl', 'shiftr', 'sign', 'sin', 'sinh', 'size', 'sngl',
'spacing', 'spread', 'sqrt', 'status', 'storage_size', 'subroutine', 'sum', 'system_clock', 'tan', 'tanh', 'target', 'this_image', 'tiny', 'to', 'trailz', 'transfer', 'transpose', 'trim',
'type', 'ubound', 'ucobound', 'unformatted', 'unit', 'unpack', 'use', 'value', 'verify', 'volatile', 'wait', 'where', 'while'] 
