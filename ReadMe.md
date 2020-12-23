# usdt demo

Linux 下静态定义探针示例.

## 依赖

CentOS-7 系统, 安装 `systemtap`, `systemtap-sdt-devel`, `bcc-tools`, `bpftrace-tools`.

```bash
yum install -y systemtap systemtap-runtime systemtap-devel systemtap-sdt-devel
yum install -y kernel-devel kernel-debug-devel bpftrace bpftrace-tools bpftrace-docs bcc-static bcc-tools
```

## 测试

```bash
make

./demo >/dev/null &

python trace.py --pid 5180

```
