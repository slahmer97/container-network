sudo bpftrace -e '
#include <linux/skbuff.h>
#include <net/ip.h>

kprobe:ip_forward {
    $skb = (struct sk_buff *)arg0;  // Get sk_buff from arg0
    $iph = (struct iphdr *)($skb->head + $skb->network_header);  // Access IP header using network_header offset

    $src = $iph->saddr;  // Source IP address
    $dst = $iph->daddr;  // Destination IP address

    printf("ip_forward called: src=%d.%d.%d.%d -> dst=%d.%d.%d.%d, packet length: %d bytes\n",
        $src & 0xFF, ($src >> 8) & 0xFF, ($src >> 16) & 0xFF, ($src >> 24) & 0xFF,
        $dst & 0xFF, ($dst >> 8) & 0xFF, ($dst >> 16) & 0xFF, ($dst >> 24) & 0xFF,
        $skb->len);
}
'
