import m5
from m5.objects import Cache
m5.util.addToPath("../../")
from common import SimpleOpts


class L1Cache(Cache):
    """Simple L1 Cache with default values"""
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    
    def __init__(self, options=None):
        super(L1Cache, self).__init__()
        pass
    
    def connectBus(self, bus):
        """Connect this cache to a memory-side bus"""
        self.mem_side = bus.cpu_side_ports
    
    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU-side port
        This must be defined in a subclass"""
        raise NotImplementedError

class L1ICache(L1Cache):
    """Simple L1 instruction cache with default values"""
    
    # Set the default size
    size = "16kB"
    
    SimpleOpts.add_option(
        "--l1i_size", help="L1 instruction cache size. Default: %s" % size
    )
   
    def __init__(self, options=None):
        super(L1ICache, self).__init__(options)
        if not options or not options.l1i_size:
            return
        self.size = options.l1i_size
    
    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU icache port"""
        self.cpu_side = cpu.icache_port
    

class L1DCache(L1Cache):
    """Simple L1 data cache with default values"""
    
    # Set the default size
    size = "64kB"
    
    SimpleOpts.add_option(
        "--l1d_size", help="L1 data cache size. Default: %s" % size
    )
    
    def __init__(self, options=None):
        super(L1DCache, self).__init__(options)
        if not options or not options.l1d_size:
            return
        self.size = options.l1d_size
    
    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU dcache port"""
        self.cpu_side = cpu.dcache_port

class L2Cache(Cache):
    """Simple L2 Cache with default values"""
    
    # Default parameters
    size = "256kB"
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12
    
    SimpleOpts.add_option(
        "--l2_size", help="L2 cache size. Default: %s" % size
    )
    
    def __init__(self, options=None):
        super(L2Cache, self).__init__()
        if not options or not options.l2_size:
            return
        self.size = options.l2_size
    
    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports
    
    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports