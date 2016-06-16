import numpy as np
import cv2
#import SimpleITK as sitk
import tifffile


def hist(src, weights=None, bins=None, range=None, zeros=True):
    if not zeros:
        h, _ = np.histogram(src[src != 0].flatten(), weights = weights[src != 0].flatten(), normed=True, bins=bins, range=range)
    else:
        h, _ = np.histogram(src.flatten(), weights = weights.flatten(), normed=True, bins=bins, range=range)
    return h

def downsample(src):
    return cv2.pyrDown(src) 

def saveData(filename,obj):
    tifffile.imsave(filename,obj) 

def loadData(filename):       
    bigtif = tifffile.imread(filename)
    print filename+" loaded",bigtif.shape
    return bigtif.squeeze() 
    
class ImageSequence:
    def __init__(self, im):
        self.im = im
    def __getitem__(self, ix):
        try:
            if ix:
                self.im.seek(ix)
            return self.im
        except EOFError:
            raise IndexError # end of sequence   
    
def pilLoadData(filename):
    from PIL import Image
    im = Image.open(filename)
    bigtif = np.concatenate([np.array(frame)[np.newaxis,:,:] for frame in ImageSequence(im)], axis=0)
    print filename+" loaded (PIL)", bigtif.shape
    return bigtif.squeeze()

def norm(img,minval=None,maxval=None):
    out = np.array(img,dtype='float32',copy=True)
    if not minval: minval = out.min()
    if not maxval: maxval = out.max()
    out -= minval
    out /= maxval - minval
    
    out[out > 1] = 1 
    return out
    
def subtractBackground(img,window=30):
    #mins = np.array(img,dtype='float32',copy=True)
    #for x in range(0,img.shape[0]):
    #    for y in range(0,img.shape[1]):               
    #        mins[x,y] = img[ max(0,x - window/2):min(img.shape[0],x + window/2), max(0, y - window/2):min(img.shape[1],y + window/2)].min()
    #    print(x,img.shape[0])
    
    st = cv2.getStructuringElement(cv2.MORPH_RECT, (window, window))
    mins = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, st, iterations=1)    

    #saveData('tempBack.tif',mins.astype(np.float32)) 

    return mins#img-mins
    
def smallBlur(img, pixels=3):
    return cv2.GaussianBlur(np.array(img,dtype='float32'), (0,0), pixels)
        
    
def normMean(img):
    out = np.array(img,dtype='float32',copy=True)
    out /= out.std()
    out /= 5
    out -= out.mean()
    out += 0.5 #arbitrary, but shouldn't matter all that much what it is                 
    out[out > 1] = 1 
    out[out < 0] = 0 
    return out    
    
def preprocess(img, size = 20, bs = 'tophat', curveblur=False, init_blur = True):
    small = smallBlur(img) if init_blur else img
    
    
    if bs=='blur':
        big = cv2.GaussianBlur(np.array(img,dtype='float32'), (0,0), size)
        big = small / big
        big /= big.max()
    else:
        big=small
    
    if bs == 'tophat':
        st = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
        big = cv2.morphologyEx(big, cv2.MORPH_TOPHAT, st, iterations=3)
        
        #sitk version of tophat.  Very slow and ugly.
        #pimg = sitk.GetImageFromArray(big)
        #thFilter = sitk.WhiteTopHatImageFilter()
        #thFilter.SetKernelRadius( size )
        #cimg = thFilter.Execute( pimg )
        #big = sitk.GetArrayFromImage( cimg )        
        
    
    '''if curveblur:
        #
        # Blur using CurvatureFlowImageFilter
        #
        iterations = 50#75
        pimg = sitk.GetImageFromArray(big)

        #blurFilter = sitk.MinMaxCurvatureFlowImageFilter()
        #blurFilter.SetStencilRadius( 50 )
        blurFilter = sitk.CurvatureFlowImageFilter()
        blurFilter.SetNumberOfIterations( iterations )
        blurFilter.SetTimeStep( 0.25 )
        cimg = blurFilter.Execute( pimg )
        tc5b = sitk.GetArrayFromImage( cimg )
        
        big = tc5b'''
            
    return big    
    
def conv16to8(image, display_min, display_max): # copied from Bi Rico (stackexchange)
    # Here I set copy=True in order to ensure the original image is not
    # modified. If you don't mind modifying the original image, you can
    # set copy=False or skip this step.
    image = np.array(image, copy=True)
    image.clip(display_min, display_max, out=image)
    image -= display_min
    image //= (display_max - display_min + 1) / 256.
    return image.astype(np.uint8)

    
