# bwauth Analyses

Archived here for posterity. The most recent addition is at the top.

* <a href="#cdn">Single Server vs CDN</a>
* <a href="#updated-01">Updated Comparisons</a>
* <a href="#scanner-loop-times-and-dns">Scanner Loop Times and DNS</a>
* <a href="#fast-relays-vs-all-relays">Fast Relays vs All Relays</a>
* <a href="#dns-measurements">DNS Measurements</a>
* <a href="#apples-to-apples-comparison">Apples to Apples Comparison</a>

## Single Server vs CDN

Over in [this ticket](https://trac.torproject.org/projects/tor/ticket/24506) we were wondering how much of a difference using a CDN makes for the bwauth measurements. We used fastly as the CDN.

Note that this graph only compares the difference using a CDN makes for _this one bwauth_. As shown in [the geographic bwauth bandwidth weighting graph](https://people.torproject.org/~irl/volatile/rsvotes/) (that link may be temporary, but it works right now) - different bwauths generally weight geographic weights differently.

Also, as shown by the graph in section right before this one, it seems like the network as a whole may be getting a little 'more different' recently, so that should be considered. (We may be reaching the limits of how good of conclusions we can draw from "Well we'll just graph it, and see if it looks weird!")

![CDN Comparison](https://tomrittervg.github.io/bwauth-tools/analyses/fastly-01.png)

## Updated Comparisons

As a followup to the earlier per-bwauth comparisons, here are updated graphs.

All bwauths, but not breaking out fast relays:
![bwauth comparisons, Jan 2018](https://tomrittervg.github.io/bwauth-tools/analyses/all-no-hundred-02.png)

Comparison to moria:
![Comparison to moria](https://tomrittervg.github.io/bwauth-tools/analyses/hundred-moria-02.png)

Comparison to bastet:
![Comparison to moria](https://tomrittervg.github.io/bwauth-tools/analyses/hundred-bastet-02.png)

Comparison to gabelmoo:
![Comparison to gabelmoo](https://tomrittervg.github.io/bwauth-tools/analyses/hundred-gabelmoo-02.png)

I lost data for faravahar in November unfortunetly, but hope to get it back soon.


## Scanner Loop Times and DNS 

When we were looking at [https://trac.torproject.org/projects/tor/ticket/21394 the DNS timeout issue], Sebastian had the question if the IP-based scanners completed faster. I publish the scanner loop times for the purposes of detecting a stuck scanner, so I could measure the time between a DNS-based bwauth and an IP-address based bwauth.

The graphs are below. In order to make them quickly I don't have the X axis labeled very nicely, but here's what it means:

* 1 means the DNS-based Scanner
* 1.5 is the *average* of the DNS-based Scanner
* 2 means the IP-based Scanner
* 2.5 is the *average* of the IP-based Scanner

![Scanner 1](https://tomrittervg.github.io/bwauth-tools/analyses/scanner-1.png)

![Scanner 2](https://tomrittervg.github.io/bwauth-tools/analyses/scanner-2.png)

![Scanner 3](https://tomrittervg.github.io/bwauth-tools/analyses/scanner-3.png)

![Scanner 4](https://tomrittervg.github.io/bwauth-tools/analyses/scanner-4.png)

![Scanner 5](https://tomrittervg.github.io/bwauth-tools/analyses/scanner-5.png)

![Scanner 6](https://tomrittervg.github.io/bwauth-tools/analyses/scanner-6.png)

![Scanner 7](https://tomrittervg.github.io/bwauth-tools/analyses/scanner-7.png)

![Scanner 8](https://tomrittervg.github.io/bwauth-tools/analyses/scanner-8.png)

![Scanner 9](https://tomrittervg.github.io/bwauth-tools/analyses/scanner-9.png)

Based on this data, it seems like Scanner 1 and maybe 2 are impacted by this, but for the rest, they seem like within just random variation.  That makes sense - the fastest relays are the ones that experience DNS timeouts (and hence longer scanner times.)

## Fast Relays vs All Relays

I had a theory: fast relays speed is more stable, while slow relays (really relays in the bottom bucket of slowness) have more volatile speeds. One bwauth measures them at 25, another bwauth measured them at 50 - a 100% difference. So I queried twice, once for all relays, and once for relays whose speed (in both consensuses) was > 100.

Here I compare maatuska's bwauth to each other bwauth:

Comparison to maatuska's alternate bwauth:
![Comparison to maatuska's alternate bwauth](https://tomrittervg.github.io/bwauth-tools/analyses/hundred-maatuska-01.png)

Comparison to moria:
![Comparison to moria](https://tomrittervg.github.io/bwauth-tools/analyses/hundred-moria-01.png)

Comparison to faravahar:
![Comparison to moria](https://tomrittervg.github.io/bwauth-tools/analyses/hundred-faravahar-01.png)

Comparison to bastet:
![Comparison to moria](https://tomrittervg.github.io/bwauth-tools/analyses/hundred-bastet-01.png)

What is up with bastet! This one requires more investigation!


But in general, there is not much difference between the top relays and the bottom relays. Aside from whatever happened to bastet!

## DNS Measurements

As part of the investigation of [https://trac.torproject.org/projects/tor/ticket/21394 the DNS timeout issue], bwauths were asked to make sure they were conducting measurements using a DNS name as the download location and not an IP address. The thinking was if an exit has DNS timeouts, its measured bandwidth rating should go down. My bwauth was already using a DNS name, but I switched the alternate bwauth to use an IP address to compare.

![DNS vs IP address comparison](https://tomrittervg.github.io/bwauth-tools/analyses/dns-comparison-01.png)

I ran two bwauths, that had no differences between them, and calculated the average difference between two sets of relays for each consensus: the set of all relays, and the set of relays where the bw measurement was above 100 in both bwauths. That data (the blue and green lines) are the control.

Then I changed one bwauth to connect to the final destination using an IP address and left the other one connecting using a DNS name. That data is the the orange and red lines.

I don't see much of a difference. So it seems that bwauth measurements were not affected by this issue.

## Apples to Apples comparison

I was wondering how much bwauths disgaree on measurements. That seemed interesting. But first a simpler question arose: how much does a bwauth disagree with *itself*? So I ran two identical bwauths from the same box at the same time, and compared their results.

![Two identical bwauths](https://tomrittervg.github.io/bwauth-tools/analyses/straight-comparison-01.png)

The >100 graph restricts the calculations only to relays whose bw value (measured by both bwauths) is at least 100. It turns out there is quite a bit of difference!