# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 10:32:52 2017

@author: m.leclech
"""

import os
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras_adversarial import simple_gan, gan_targets
from keras_adversarial import AdversarialOptimizerSimultaneous
from keras.optimizers import Adam




def model_generator(nb_words, nb_features):
    return Sequential([
        Dense(nb_features, name="generator_h1", input_shape=(nb_words, nb_features), activation='relu'),
        Dense(int(nb_features/2), name="generator_h2", activation='relu'),
        Dense(1, name="generator_h3", activation='sigmoid'),
        ], name="generator")
        
def model_discriminator(nb_words, nb_features):
    return Sequential([
        Dense(nb_features, name="discriminator_h1", input_shape=(nb_words, nb_features), activation='relu'),
        Dense(int(nb_features/2), name="discriminator_h2", activation='relu'),
        Flatten(name="discriminator_flatten"),
        Dense(int(nb_features*nb_words/4), name="discriminator_h3", activation='relu'),
        Dense(1, name="discriminator_h4"),
        ], name="discriminator")
        
def gan(adversarial_optimizer, path, opt_g, opt_d, nb_epoch, generator, discriminator,
                targets=gan_targets, loss='binary_crossentropy'):

    print("ok3")
    # gan (x - > yfake, yreal), z generated on GPU
    gan = simple_gan(generator, discriminator, None)
    print("ok4")

    # print summary of models
    generator.summary()
    discriminator.summary()
    gan.summary()
    print("ok5")

    # build adversarial model
    model = AdversarialModel(base_model=gan,
                             player_params=[generator.trainable_weights, discriminator.trainable_weights],
                             player_names=["generator", "discriminator"])
    model.adversarial_compile(adversarial_optimizer=adversarial_optimizer,
                              player_optimizers=[opt_g, opt_d],
                              loss=loss)

    # create callback to generate images
    zsamples = np.random.normal(size=(10 * 10, latent_dim))

    def generator_sampler():
        return generator.predict(zsamples).reshape((10, 10, 28, 28))

    generator_cb = ImageGridCallback(os.path.join(path, "epoch-{:03d}.png"), generator_sampler)

    # train model
    xtrain, xtest = mnist_data()
    y = targets(xtrain.shape[0])
    ytest = targets(xtest.shape[0])
    callbacks = [generator_cb]
    if K.backend() == "tensorflow":
        callbacks.append(
            TensorBoard(log_dir=os.path.join(path, 'logs'), histogram_freq=0, write_graph=True, write_images=True))
    history = fit(model, x=xtrain, y=y, validation_data=(xtest, ytest), callbacks=callbacks, nb_epoch=nb_epoch,
                  batch_size=32)

    # save models
    generator.save(os.path.join(path, "generator.h5"))
    discriminator.save(os.path.join(path, "discriminator.h5"))
    
def main():
    nb_mots = 30
    nb_features = 91
    generator = model_generator(nb_mots, nb_features)
    print("ok1")
    discriminator = model_discriminator(nb_mots, nb_features)
    print("ok2")
    gan(AdversarialOptimizerSimultaneous(), os.path.join("output", "ganRNN"),
                opt_g=Adam(1e-4, decay=1e-4),
                opt_d=Adam(1e-3, decay=1e-4),
                nb_epoch=100, generator=generator, discriminator=discriminator,)


if __name__ == "__main__":
    main()