#pragma once
// Helpers for preview.yaml, the host build of the clock face.
#include <sys/time.h>
#include <SDL.h>
#include <cstdio>
#include <cstdlib>

// Saves the preview window to $CLOCK_PREVIEW_OUT/<name>.bmp. Does nothing
// when CLOCK_PREVIEW_OUT is not set, so an interactive run just shows the face.
inline void preview_save(const char *name) {
  const char *dir = getenv("CLOCK_PREVIEW_OUT");
  SDL_Window *window = SDL_GetWindowFromID(1);
  if (dir == nullptr || window == nullptr)
    return;
  SDL_Renderer *renderer = SDL_GetRenderer(window);
  int w, h;
  SDL_GetRendererOutputSize(renderer, &w, &h);
  SDL_Surface *surface = SDL_CreateRGBSurfaceWithFormat(0, w, h, 32, SDL_PIXELFORMAT_ARGB8888);
  SDL_RenderReadPixels(renderer, nullptr, SDL_PIXELFORMAT_ARGB8888, surface->pixels, surface->pitch);
  char path[512];
  snprintf(path, sizeof(path), "%s/%s.bmp", dir, name);
  SDL_SaveBMP(surface, path);
  SDL_FreeSurface(surface);
}

// Exits after the screenshots are saved, when CLOCK_PREVIEW_OUT is set.
inline void preview_done() {
  if (getenv("CLOCK_PREVIEW_OUT") != nullptr)
    exit(0);
}
