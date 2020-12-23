#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "probes.h"

void foo(int a, int b) {
    // 添加探针
    // 1. 原始方式
    // DTRACE_PROBE2(demo, foo, a, b);
    // 2. 使用 dtrace 生成辅助宏
    if (DEMO_FOO_ENABLED()) {
        DEMO_FOO(a, b);
    }

    printf("a:%d b:%d\n", a, b);
}

int main() {
    int a = 10;
    int b = 20;

    int i = 0;
    for (i = 0; i < 1000; i++) {
        foo(a, b);
        sleep(5);
    }

    return 0;
}
