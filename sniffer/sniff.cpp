
/*

 // open device
 pcap_open_live()

 // set non-block
 pcap_setnonblock()

 // figure datalink package type
 pcap_datalink()

 // change channel
 iwconfig <en0> channel channel_no

 // capture package
 pcap_dispatch() // non-blocking
 pcap_loop() // blocking

 // handle package depend on type of datalink header type


*/
#include <pcap/pcap.h>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <libpq-fe.h>

using namespace std;

pcap_t* handle;
int datalink;


void set_moniter_mode(char* dev) {

#ifdef __APPLE__
    /*
     * airport <en0> sniff 1
     */
#elif __linux__
    /*
     *
     * iwconfig <en0> mode moniter
     *
     * if failed
     *      ifconfig <en0> down
     *      iwconfig <en0> mode moniter
     *      ifconfig <en0> up
     */
#endif
}

void init() {
    /*
	char errbuff[BUFSIZ];
    char* dev;
    dev = pcap_lookupdev(errbuff);
    cout << "Sniff on " << dev << endl;
    set_moniter_mode(dev);

    handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuff);

    datalink = pcap_datalink(handle);
    cout << datalink << endl;
*/
	}

void capture_package() {

}

void package_handler() {

}

void change_channel(int channel_no) {

}


int main() {
    init();
    return 0;
}
