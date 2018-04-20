from scipy.io import wavfile
import numpy as np
import pylab as pl
from sklearn.decomposition import FastICA


fs_1, voice_1 = wavfile.read("mix_type_1_1.wav")
fs_2, voice_2 = wavfile.read("mix_type_1_2.wav")
m, = voice_1.shape
voice_2 = voice_2[:m]


S = np.c_[voice_1, voice_2]
A = np.array([[1, 1], [0.5, 2]])  # Mixing matrix
X = np.dot(S, A.T)  # Generate observations
# Compute ICA
ica = FastICA()
S_ = ica.fit(X).transform(X)  # Get the estimated sources
A_ = ica.mixing_  # Get estimated mixing matrix
np.allclose(X, np.dot(S_, A_.T))

multiply_factor = 1000000 ;

temp_output_1 = multiply_factor*S_[:,0]
temp_output_2 = multiply_factor*S_[:,1]

wavfile.write("Seperated_1" + ".wav", fs_2, temp_output_1.astype(np.int16))
wavfile.write("Seperated_2" + ".wav", fs_2, temp_output_2.astype(np.int16))


# Plot results
pl.figure()
pl.subplot(3, 1, 1)
pl.plot(S)
pl.title('True Sources')
pl.subplot(3, 1, 2)
pl.plot(X)
pl.title('Observations (mixed signal)')
pl.subplot(3, 1, 3)
pl.plot(S_)
pl.title('ICA estimated sources')
pl.subplots_adjust(0.09, 0.04, 0.94, 0.94, 0.26, 0.36)
pl.show()

