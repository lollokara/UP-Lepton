/*#
# Project: Lepton Streaming and recording with Flask
# Author: lorenzo [at] karavania [dot] com>
# Date: 2016/11/2
# Website: http://karavania.com
#*/

#include<stdio.h>
#include<signal.h>
#include<unistd.h>
#include<mraa.h>

void sig_handler(int signum);
void save_pgm_file();
static sig_atomic_t volatile isrunning = 1;
static unsigned int image[80*60];

main(int argc, char **argv)
{
	signal(SIGINT, &sig_handler);
    mraa_init();
	mraa_gpio_context cs = mraa_gpio_init(24);
	mraa_gpio_dir(cs, MRAA_GPIO_OUT);
	mraa_spi_context spi = mraa_spi_init(0);
	mraa_spi_mode(spi, MRAA_SPI_MODE3);
	mraa_spi_frequency(spi, 6250000);
	mraa_spi_lsbmode(spi, 0);
	mraa_spi_bit_per_word(spi, 8);
	uint8_t payload[164];
	uint8_t *recv = NULL;
	int packetNb;
	int i;
	uint8_t checkByte = 0x0f;
	mraa_gpio_write(cs, 1);
	usleep(60000); //play around for stability
	mraa_gpio_write(cs, 0);
    while((checkByte & 0x0f) == 0x0f && isrunning){
		if(recv)
			free(recv);
		recv = mraa_spi_write_buf(spi, payload, 164);
		checkByte = recv[0];
		packetNb = recv[1];
	}
	while(packetNb < 60 && isrunning)
	{
		if((recv[0] & 0x0f) != 0x0f){
			for(i=0;i<80;i++)
			{
				image[packetNb * 80 + i] = (recv[2*i+4] << 8 | recv[2*i+5]);
			}
		}
		if(recv)
			free(recv);
		recv = mraa_spi_write_buf(spi, payload, 164);
		packetNb = recv[1];
	}

	save_pgm_file();
    mraa_gpio_write(cs, 1);
	return MRAA_SUCCESS;
}

void save_pgm_file()
{
	int i;
	int j;
	unsigned int maxval = 0;
	unsigned int minval = 100000;
    
	FILE *f = fopen("imageResized.pgm", "w");
    
	if (f == NULL)
	{
		printf("Error opening file!\n");
		exit(1);
	}

    for(i=0;i<60;i++)
	{
		for(j=0;j<80;j++)
		{
			if (image[i * 80 + j] > maxval) {
				maxval = image[i * 80 + j];
			}
			if (image[i * 80 + j] < minval) {
				minval = image[i * 80 + j];
			}
		}
	}
    
	///printf("maxval = %u\n",maxval);
	///printf("minval = %u\n",minval);
    
    
	fprintf(f,"P2\n80 60\n%u\n",maxval-minval);
	for(i=0;i<60;i++)
	{
		for(j=0;j<80;j++)
		{
			fprintf(f,"%d ", image[i * 80 + j] - minval);
		}
		fprintf(f,"\n");
	}
	fprintf(f,"\n\n");
	fclose(f);
    FILE *f2 = fopen("image.txt", "w");
    
    if (f2 == NULL)
    {
        printf("Error opening file!\n");
        exit(1);
    }
    fprintf(f,"%d",maxval);
    fclose(f2);

    
}

void sig_handler(int signum)
{
	if(signum == SIGINT)
		isrunning = 0;
}
