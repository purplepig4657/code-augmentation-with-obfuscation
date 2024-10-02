import regex

class Preprocessor:
    GENERATED_STRUCTS = [
        '_IO_FILE', 'timeval', '__sFILE', '__sFILEX', '__sbuf',
        '__anonstruct__RuneCharClass', '__anonstruct__RuneEntry',
        '__anonstruct__RuneLocale', '__anonstruct__RuneRange', 'timespec',
        '__locale_data', '_IO_codecvt', '_IO_marker', '_IO_wide_data', 'sigevent',
        '__locale_struct', '_ymmh_state', '__anonstruct___once_flag', 
        '__anonstruct__timer', 'tm', '__anonstruct_lldiv_t', '_G_fpos_t', '_libc_xmmreg',
        '__anonstruct__kill', '__pthread_cond_s', '_xstate',
        '__anonstruct__sigchld', '_libc_fpxreg', '__anonstruct__rt',
        '__anonstruct_mcontext_t', '__anonstruct___value', '_xmmreg',
        '__anonstruct_ldiv_t', '_fpreg', '__anonstruct_fenv_t',
        '__anonstruct___sigset_t', '__anonstruct__sigpoll',
        '__anonstruct_imaxdiv_t', '__anonstruct__addr_bnd', 'random_data',
        '_libc_fpstate', '_xsave_hdr', '_fpx_sw_bytes', '__anonstruct_div_t',
        '__anonstruct_siginfo_t', 'drand48_data', '__pthread_internal_slist',
        '__anonstruct__sigfault', '__anonstruct__sigsys', '_G_fpos64_t',
        '__pthread_rwlock_arch_t', '_fpxreg', 'itimerspec', '__anonstruct___mbstate_t',
        'sigaction', '__anonstruct___fsid_t', '__anonstruct_stack_t',
        'sigstack', 'lconv', '__anonstruct__sigev_thread', '__pthread_mutex_s',
        'sigcontext', '__anonstruct_fd_set', '__anonstruct_max_align_t',
        '__pthread_internal_list', '_fpstate', '__jmp_buf_tag', 'ucontext_t',
        '__anonstruct___once_flag', '__anonstruct___value32'
    ]
    TYPEDEF_KEYWORDS = [
        'wint_t', '__uint32_t', 'fpos_t', 'wctype_t', '__mode_t', '__u_quad_t', '__u_int',
        'u_int', 'int_fast16_t', '__ino_t', 'ino_t', '_Float64', '__blksize_t', 'blksize_t',
        '__daddr_t', 'daddr_t' '__locale_t', 'locale_t', 'wchar_t',
        '__fsfilcnt_t', 'fsfilcnt_t', '__int32_t', '__time_t', 'time_t', '__nlink_t',
        'nlink_t', '__int8_t', '__int_least8_t', 'int_least8_t', '__uint64_t',
        '__fd_mask', '__off64_t', '__uint8_t', '__uint_least8_t', '__intmax_t', 'intmax_t',
        'fexcept_t', '__sigset_t', 'sigset_t', '__ssize_t', '__clockid_t', 'mbstate_t',
        '__uint16_t', '__gnuc_va_list', '__key_t', 'key_t', '__fsblkcnt_t', 'fsblkcnt_t',
        'pthread_spinlock_t', 'int_fast32_t', '__off_t', '__sigval_t', 'sigval_t',
        '__jmp_buf', '_Float32x', 'register_t', 'sigjmp_buf', 'wctrans_t', '__clock_t',
        '__pid_t', '__uid_t', 'uint_least32_t', '__id_t', 'fpregset_t', '__int16_t', 'int16_t',
        '__gwchar_t', 'id_t', '__compar_fn_t', '__int_least16_t', '__rlim64_t',
        '__blkcnt64_t', '__int64_t', '__int_least64_t', 'int_least64_t', '__suseconds_t',
        'int64_t', '_IO_lock_t', '__syscall_slong_t', 'pthread_once_t', 'uint_least64_t',
        '__u_char', 'u_char', '__rlim_t', '__uintmax_t', '_Float32', '__timer_t', 'timer_t',
        'intptr_t', '__sighandler_t', 'uintptr_t', 'greg_t', 'gregset_t',
        'fsid_t', '__caddr_t', 'caddr_t', '__gid_t', 'gid_t', '__u_long', 'int_least32_t',
        'uint_fast64_t', '__sig_atomic_t', 'sig_atomic_t', '__u_short', 'u_short',
        '__quad_t', 'quad_t', 'ushort', '__suseconds64_t', 'uint_fast8_t', 'ptrdiff_t',
        'int_fast8_t', 'uint_fast16_t', '__blkcnt_t', '__ino64_t', 'ulong', '__tss_t',
        '__dev_t', 'dev_t', 'uint', 'pthread_key_t', 'loff_t', '__useconds_t',
        '__fsblkcnt64_t', '__thrd_t', 'va_list', '__socklen_t', 'int_fast64_t',
        'uint_least16_t', '__fsfilcnt64_t', 'blkcnt_t', 'uint_fast32_t',
        'wctrans_t', '__compar_fn_t', '__timer_t', '__sighandler_t', '__caddr_t',
        'sig_t', '__syscall_ulong_t', '__intptr_t', 'pthread_t', '__fsword_t'
    ]
    GENERATED_UNIONS = [
        'pthread_attr_t', '__anonunion_pthread_rwlock_t',
        '__anonunion__sigev_un', '__anonunion_pthread_condattr_t',
        '__anonunion___atomic_wide_counter',
        '__anonunion____missing_field_name',
        '__anonunion_pthread_barrier_t', 'sigval',
        '__anonunion__sifields', '__anonunion_pthread_mutexattr_t',
        '__anonunion_pthread_rwlockattr_t',
        '__anonunion_pthread_barrierattr_t',
        '__anonunion_pthread_mutex_t', '__anonunion__bounds',
        '__anonunion___sigaction_handler', '__anonunion___value',
        '__anonunion_pthread_cond_t', '__anonunion___atomic_wide_counter',
    ]
    GENERATED_ENUMS = [
        '__anonenum'
    ]

    def __init__(
        self,
        remove_extern: bool = True,
        remove_generated_struct: bool = True,
        remove_typedefs: bool = True,
        remove_comments: bool = True,
        remove_inline_functions: bool = True,
    ):
        self.remove_extern = remove_extern
        self.remove_generated_struct = remove_generated_struct
        self.remove_typedefs = remove_typedefs
        self.remove_comments = remove_comments
        self.remove_inline_functions = remove_inline_functions

    def preprocess(self, file: str) -> bool:
        with open(file, 'r') as f:
            content = f.read()

        if self.remove_extern:
            content = regex.sub(r'^extern[\s\S]*?;[\s\n]*', '', content, flags=regex.MULTILINE)
            content = regex.sub(r'^__inline\s+extern[\s\S]*?(?:;|(\{(?:[^{}]++|(?1))*\}))[\s\n]*', '', content, flags=regex.MULTILINE)

        if self.remove_inline_functions:
            content = regex.sub(r'^__inline\s+static[\s\S]*?(?:;|(\{(?:[^{}]++|(?1))*\}))[\s\n]*', '', content, flags=regex.MULTILINE)

        if self.remove_comments:
            content = regex.sub(r'//.*$', '', content, flags=regex.MULTILINE)
            content = regex.sub(r'/\*[\s\S]*?\*/', '', content)

        if self.remove_generated_struct:
            for struct_name in self.GENERATED_STRUCTS:
                content = regex.sub(rf'struct\s+{struct_name}(?:_\d+)?\s*;\n', '', content)
                content = regex.sub(rf'struct\s+{struct_name}(?:_\d+)?\s*\{{[^}}]*\}};\n', '', content)
                content = regex.sub(rf'typedef\s+struct\s+{struct_name}(?:_\d+)?\s+\*?\s*\w+;\n', '', content)
            
            for union_name in self.GENERATED_UNIONS:
                content = regex.sub(rf'union\s+{union_name}(?:_\d+)?\s*;\n', '', content)
                content = regex.sub(rf'union\s+{union_name}(?:_\d+)?\s*\{{[^}}]*\}};\n', '', content)
                content = regex.sub(rf'typedef\s+union\s+{union_name}(?:_\d+)?\s+\*?\s*\w+;\n', '', content)
            
            for enum_name in self.GENERATED_ENUMS:
                content = regex.sub(rf'enum\s+{enum_name}(?:_\d+)?\s*;\n', '', content)
                content = regex.sub(rf'enum\s+{enum_name}(?:_\d+)?\s*\{{[\s\S]*?\}}[;\s]*', '', content)
                content = regex.sub(rf'typedef\s+enum\s+{enum_name}(?:_\d+)?\s+\*?\s*\w+;\n', '', content)

        if self.remove_typedefs:
            # Updated pattern to handle all types of typedefs
            typedef_pattern = r'typedef\s+(?:(?:(?:unsigned|signed|volatile|const)\s+)?(?:\w+\s+)*(?:' + '|'.join(self.TYPEDEF_KEYWORDS) + r'|void|char)\s*(?:const\s+)?\**\s*)(?:\w+\s*)*(?:\[[\w\s]*\])?;'
            content = regex.sub(typedef_pattern, '', content)

            # Additional pattern for function pointer typedefs
            func_ptr_pattern = r'typedef\s+(?:\w+\s+)*\(\*\w+\)\s*\([^)]*\)\s*;'
            content = regex.sub(func_ptr_pattern, '', content)

        with open(file, 'w') as f:
            f.write(content)

        # Remove empty lines
        with open(file, 'r') as f:
            lines = f.readlines()

        # Remove lines that are empty or contain only whitespace
        lines = [line for line in lines if line.strip()]

        with open(file, 'w') as f:
            f.writelines(lines)

        return True
