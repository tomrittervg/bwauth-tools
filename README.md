# bwauth Analyses

Archived here for posterity

## Apples to Apples comparison

I was wondering how much bwauths disgaree on measurements. That seemed interesting. But first a simpler question arose: how much does a bwauth disagree with *itself*? So I ran two identical bwauths from the same box at the same time, and compared their results.

![Two identical bwauths](https://tomrittervg.github.io/bwauth-tools/analyses/straight-comparison-01.png)

The >100 graph restricts the calculations only to relays whose bw value (measured by both bwauths) is at least 100. It turns out there is quite a bit of difference!

## DNS Measurements

As part of the investigation of [https://trac.torproject.org/projects/tor/ticket/21394 the DNS timeout issue], bwauths were asked to make sure they were conducting measurements using a DNS name as the download location and not an IP address. The thinking was if an exit has DNS timeouts, its measured bandwidth rating should go down. My bwauth was already using a DNS name, but I switched the alternate bwauth to use an IP address to compare.

![DNS vs IP address comparison](https://tomrittervg.github.io/bwauth-tools/analyses/dns-comparison-01.png)

I ran two bwauths, that had no differences between them, and calculated the average difference between two sets of relays for each consensus: the set of all relays, and the set of relays where the bw measurement was above 100 in both bwauths. That data (the blue and green lines) are the control.

Then I changed one bwauth to connect to the final destination using an IP address and left the other one connecting using a DNS name. That data is the the orange and red lines.

I don't see much of a difference. So it seems that bwauth measurements were not affected by this issue.