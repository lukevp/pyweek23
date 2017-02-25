import pygame
font_root = "assets/fonts/"
def get_font(text, fontname, size, color, bgcolor=(0,0,0)):
    font = pygame.font.Font(font_root + fontname, 240)
    surf = font.render(text, True, color, bgcolor)
    surf = surf.convert(32)
    return surf

def aspect_scale(img,(bx,by)):
    """ Scales 'img' to fit into box bx/by.
     This method will retain the original image's aspect ratio """
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (int(sx),int(sy)))

def scale_rect(screen_rect, source_rect, widthpct, heightpct):
    #to make a rect that is 60% of the width, get the current rect, and determine the scale ratio between full screen and
    # current width, then scale to full width, then multiply by scale ratio.
    scale_factor =  screen_rect.width / float(source_rect.width)
    newrect = pygame.rect.Rect(0, 0, source_rect.width * scale_factor * widthpct, source_rect.height * scale_factor * heightpct)
    return newrect
    #TODO: handle height scaling too.