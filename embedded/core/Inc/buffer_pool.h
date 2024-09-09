
#ifndef __BUFFER_POOL_H
#define __BUFFER_POOL_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>

#define BUFFER_POOL_MAX_BUFFERS 10
#define NUM_SAMPLES 10
#define NUM_CHANNELS 3

typedef struct {
	size_t allocated_buffers;
	size_t used_buffers;

	uint16_t *free[BUFFER_POOL_MAX_BUFFERS ];
} buffer_pool_t;

void buffer_pool_free(buffer_pool_t *pool, uint16_t *buf);
uint16_t *buffer_pool_allocate(buffer_pool_t* pool);



#ifdef __cplusplus
}
#endif

#endif /* __BUFFER_POOL_H */
