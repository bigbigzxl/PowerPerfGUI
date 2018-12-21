class PMU_RAW_EVENTS:
    SW_INCR                = 0
    L1I_CACHE_REFILL       = 1
    L1I_TLB_REFILL         = 2
    L1D_CACHE_REFILL       = 3
    L1D_CACHE              = 4
    L1D_TLB_REFILL         = 5
    LD_RETIRED             = 6
    ST_RETIRED             = 7
    INST_RETIRED           = 8
    EXC_TAKEN              = 9
    EXC_RETURN             = 10
    CID_WRITE_RETIRED      = 11
    PC_WRITE_RETIRED       = 12
    BR_IMMED_RETIRED       = 13
    BR_RETURN_RETIRED      = 14
    UNALIGNED_LDST_RETIRED = 15
    BR_MIS_PRED            = 16
    CPU_CYCLES             = 17
    BR_PRED                = 18
    MEM_ACCESS             = 19
    L1I_CACHE              = 20
    L1D_CACHE_WB           = 21
    L2D_CACHE              = 22
    L2D_CACHE_REFILL       = 23
    L2D_CACHE_WB           = 24
    BUS_ACCESS             = 25
    MEMORY_ERROR           = 26
    INST_SPEC              = 27
    TTBR_WRITE_RETIRED     = 28
    BUS_CYCLES             = 29
    CHAIN                  = 30
    L1D_CACHE_ALLOCATE     = 31
    # A53 support end.
    L2D_CACHE_ALLOCATE     = 32
    BR_RETIRED             = 33
    BR_MIS_PRED_RETIRED    = 34
    STALL_FRONTEND         = 35
    STALL_BACKEND          = 36
    L1D_TLB                = 37
    L1I_TLB                = 38
    L2I_CACHE              = 39
    L2I_CACHE_REFILL       = 40
    L3D_CACHE_ALLOCATE     = 41
    L3D_CACHE_REFILL       = 42
    L3D_CACHE              = 43
    L3D_CACHE_WB           = 44
    L2D_TLB_REFILL         = 45
    L2I_TLB_REFILL         = 46
    L2D_TLB                = 47
    L2I_TLB                = 48
    EventName              = [  "SW_INCR",
                                "L1I_CACHE_REFILL",
                                "L1I_TLB_REFILL",
                                "L1D_CACHE_REFILL",
                                "L1D_CACHE",

                                "L1D_TLB_REFILL",
                                "LD_RETIRED",
                                "ST_RETIRED",
                                "INST_RETIRED",
                                "EXC_TAKEN",

                                "EXC_RETURN",
                                "CID_WRITE_RETIRED",
                                "PC_WRITE_RETIRED",
                                "BR_IMMED_RETIRED",
                                "BR_RETURN_RETIRED",

                                "UNALIGNED_LDST_RETIRED",
                                "BR_MIS_PRED",
                                "CPU_CYCLES",
                                "BR_PRED",
                                "MEM_ACCESS",

                                "L1I_CACHE",
                                "L1D_CACHE_WB",
                                "L2D_CACHE",
                                "L2D_CACHE_REFILL",
                                "L2D_CACHE_WB",

                                "BUS_ACCESS",
                                "MEMORY_ERROR",
                                "INST_SPEC",
                                "TTBR_WRITE_RETIRED",
                                "BUS_CYCLES",

                                "CHAIN",
                                "L1D_CACHE_ALLOCATE",
                                # A53 support end.
                                "L2D_CACHE_ALLOCATE",
                                "BR_RETIRED",
                                "BR_MIS_PRED_RETIRED",

                                "STALL_FRONTEND",
                                "STALL_BACKEND",
                                "L1D_TLB",
                                "L1I_TLB",
                                "L2I_CACHE",

                                "L2I_CACHE_REFILL",
                                "L3D_CACHE_ALLOCATE",
                                "L3D_CACHE_REFILL",
                                "L3D_CACHE",
                                "L3D_CACHE_WB",

                                "L2D_TLB_REFILL",
                                "L2I_TLB_REFILL",
                                "L2D_TLB",
                                "L2I_TLB",
                                ]