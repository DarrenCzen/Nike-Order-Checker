# Nike-Order-Checker

Easier way to check multiple Nike.com orders.

*Requires Python 2.7 and Requests

### Setup

1. Store orders in "orders.txt" in email:ordernumber format with one order per line
2. Store proxies in "proxies.txt" in ip:host or ip:host:user:pass format with one proxy per line
3. If not using proxies and checking a large number of orders, feel free to edit the DELAY in main.py
4. Edit main.py to change DISPLAY, REMOVE_CANCELLED, DELIMITER, and REGION to your liking
5. Run main.py

### TODO

- [ ] Support for Email:Password format
- [ ] Add more accurate tracking for shipped orders
- [ ] Idk, suggest stuff to me on Twitter @DefNotAvg