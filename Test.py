from random import shuffle
import glob
imageFolderPathAni = 'C:/Users/slmoni/Documents/Uni/Introduction to Neuroscience/Neuroimaging studie/Images/Ani2'#Loading images from the Ain2 folder (animate)
STIMANI1 = glob.glob(imageFolderPathAni + '/*.JPG') 

print(STIMANI1)

shuffle(STIMANI1)

print(STIMANI1)