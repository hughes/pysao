import pyfits
import numpy
import os.path

def make_mask_from_region(img, region, header=None):
    """ image : numarray image
        region : region description in image coordinate """
    
    hdul = pyfits.HDUList()
    hdu = pyfits.PrimaryHDU()
    if header:
        hdu.header = header
    if hasattr(img, "shape"):
        shape = img.shape
    elif isinstance(img, tuple):
        shape = img
    else:
        raise "img (1st argument) must be shape (tuple) of image"
        
    hdu.data = numpy.ones(shape[-2:], dtype=numpy.uint8)
    hdul.append(hdu)

    from tempfile import mkdtemp
    temp_path = mkdtemp()

    fitsname = os.path.join(temp_path, "tmp.fits")
    regname = os.path.join(temp_path, "tmp.reg")
    maskname = os.path.join(temp_path, "mask.fits")
    #maskname = "./mask.fits"

    import os
    import shutil
    try:
        hdul.writeto(fitsname)
        open(regname, "w").write(region)

        os.system("funimage %s[@%s] %s" % (fitsname, regname, maskname))
        mask = pyfits.open(maskname)[0].data
    finally:
        shutil.rmtree(temp_path)

    # Work-around for some bug???
    m = mask.astype(numpy.bool8)
    ny, nx = m.shape
    for iy in range(ny):
        if numpy.alltrue(m[iy,:]):
            m[iy,:] = False

    return m

