#include "buffer_pool.h"

void buffer_pool_free(buffer_pool_t *pool, uint16_t *buf){
	pool->free[pool->allocated_buffers - pool->used_buffers ] = buf;
}

uint16_t *buffer_pool_allocate(buffer_pool_t *pool){
	if (pool->used_buffers < pool->allocated_buffers){
		return pool->free[pool->used_buffers++];
	}
	if (pool->allocated_buffers == BUFFER_POOL_MAX_BUFFERS){
		__asm("SVC #0");
	}

	pool->allocated_buffers++;
	return (uint16_t *)malloc(sizeof(uint16_t) * NUM_SAMPLES * NUM_CHANNELS);
}
