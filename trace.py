# coding:utf-8
from bcc import BPF, USDT
import sys
import ctypes
import argparse

bpf_text = """
#include <linux/kernel.h>
#include <uapi/linux/ptrace.h>

BPF_PERF_OUTPUT(events);

typedef struct msg_s {
    int a;
    int b;
} msg_t;

int do_trace(struct pt_regs *ctx) {
    msg_t msg = {};
    bpf_usdt_readarg(1, ctx, &msg.a);
    bpf_usdt_readarg(2, ctx, &msg.b);

    events.perf_submit(ctx, &msg, sizeof(msg));

    return 0;
};
"""

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("--pid", metavar="PID", type=int,
    nargs="?", default=0, required=True, help='profile pid')
args = parser.parse_args()

profile_pid = args.pid
if profile_pid == 0:
    print("need pid")
    sys.exit(-1)

u = USDT(pid=profile_pid)
u.enable_probe(probe="demo:foo", fn_name="do_trace")

# initialize BPF
b = BPF(text=bpf_text, usdt_contexts=[u])

class Msg(ctypes.Structure):
    _fields_ = [("a", ctypes.c_int), ("b", ctypes.c_int)]

def print_event(cpu, data, size):
    event = ctypes.cast(data, ctypes.POINTER(Msg)).contents
    print("print event a:%d b:%d" % (event.a, event.b))

b["events"].open_perf_buffer(print_event)

while True:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        break
