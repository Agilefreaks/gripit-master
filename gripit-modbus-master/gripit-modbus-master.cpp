#include <iostream>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <modbus.h>

using namespace std;

int main(int argc, char *argv[])
{
	modbus_t *ctx;
	uint16_t tab_reg[4];

	ctx = modbus_new_rtu("/dev/ttyAMA0", 19200, 'N', 8, 1);
	if (ctx == NULL) {
		fprintf(stderr, "Unable to create the libmodbus context\n");
		return -1;
	}

	struct timeval byte_timeout;
	struct timeval response_timeout;

	byte_timeout.tv_sec = 0;
	byte_timeout.tv_usec = 0;
	
	response_timeout.tv_sec = 10;
	response_timeout.tv_usec = 0;
	
	modbus_set_byte_timeout(ctx, &byte_timeout);
	modbus_set_response_timeout(ctx, &response_timeout);

	modbus_set_debug(ctx, 0xFF);
	
	int rc = modbus_set_slave(ctx, 1);

	if (rc == -1) {
		fprintf(stderr, "Invalid slave ID\n");
		modbus_free(ctx);
		return -1;
	}

	if (modbus_connect(ctx) == -1) {
		fprintf(stderr, "Connection failed: %s\n", modbus_strerror(errno));
		modbus_free(ctx);
		return -1;
	}

//	uint8_t raw_req[] = { 0x01, 0x03, 0x00, 0x01, 0x0, 0x04 };
//	uint8_t rsp[MODBUS_TCP_MAX_ADU_LENGTH];
//	
//	int req_length;
//	
//	req_length = modbus_send_raw_request(ctx, raw_req, 4 * sizeof(uint8_t));
//	modbus_receive_confirmation(ctx, rsp);
	
	
	int result = modbus_read_input_registers(ctx, 1, 4, tab_reg);

	if (result == -1) {
		fprintf(stderr, "%s\n", modbus_strerror(errno));
		return -1;
	}

	for (int i = 0; i < result; i++) {
		printf("reg[%d]=%d (0x%X)\n", i, tab_reg[i], tab_reg[i]);
	}

	printf("SUCCES !");

	modbus_close(ctx);
	modbus_free(ctx);
	return 0;
}