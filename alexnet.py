import tensorflow as tf
import numpy as np

class AlexNet(object):

  def __init__(self, x, keep_prob, num_classes, skip_layer,is_training,
               weights_path = 'DEFAULT'):
    """
    Inputs:
    - x: tf.placeholder, for the input images
    - keep_prob: tf.placeholder, for the dropout rate
    - num_classes: int, number of classes of the new dataset
    - skip_layer: list of strings, names of the layers you want to reinitialize
    - weights_path: path string, path to the pretrained weights,
                    (if bvlc_alexnet.npy is not in the same folder)
    """
    # Parse input arguments
    self.X = x
    self.NUM_CLASSES = num_classes
    self.KEEP_PROB = keep_prob
    self.SKIP_LAYER = skip_layer
    self.IS_TRAINING = is_training

    self.layerlist = ['conv1','conv2','conv3','fc4','fc5']
    self.dimension = {}
    if weights_path == 'DEFAULT':
      self.WEIGHTS_PATH = 'bvlc_alexnet.npy'
    else:
      self.WEIGHTS_PATH = weights_path

    # Call the create function to build the computational graph of AlexNet
    self.create()

  def create(self):
# def conv(x, filter_height, filter_width, num_filters, stride_y, stride_x, name,
#          padding='SAME', groups=1):
# def max_pool(x, filter_height, filter_width, stride_y, stride_x,
#              name, padding='SAME'):
    # 1st Layer: Conv (w ReLu) -> MaxPool
    print("X: ")
    print(self.X)
    print(self.X.shape)
    conv1 = conv(self.X, 5, 5, 32, 1, 1, padding = 'SAME', name = 'conv1')
    pool1 = max_pool(conv1, 3, 3, 2, 2, padding = 'SAME', name = 'pool1')
    # norm1 = lrn(pool1, 2, 2e-05, 0.75, name = 'norm1')
    print("Conv1: ")
    print(conv1.shape)
    print("Pool1: ")
    print(pool1.shape)
    self.dimension['conv1'] = [5,5,3,32]
    # 2nd Layer: Conv (w ReLu) -> AvgPool
    conv2 = conv(pool1, 5, 5, 32, 1, 1, padding = 'SAME', name = 'conv2')
    pool2 = avg_pool(conv2, 3, 3, 2, 2, padding = 'SAME', name ='pool2')
    # norm2 = lrn(pool2, 2, 2e-05, 0.75, name = 'norm2')
    print("Conv2: ")
    print(conv2.shape)
    print("Pool2: ")
    print(pool2.shape)  

    self.dimension['conv2'] = [5,5,32,32]
    # 3rd Layer: Conv (w ReLu) -> AvgPool
    conv3 = conv(pool2, 5, 5, 64, 1, 1, padding = 'SAME', name = 'conv3')
    pool3 = avg_pool(conv3, 3, 3, 2, 2, padding = 'SAME', name = 'pool3')
    print("Conv3: ")
    print(conv3.shape)
    print("Pool3: ")
    print(pool3.shape)

    self.dimension['conv3'] = [5,5,32,64]
    #350*230 temporary image crop
    flattened = tf.reshape(pool3, [-1, pool3.shape[1].value*pool3.shape[2].value*64])
    fc4 = fc(flattened, pool3.shape[1].value*pool3.shape[2].value*64, 100, name='fc4')
    dropout4 = dropout(fc4, self.KEEP_PROB)
  
    self.fc5 = fc(dropout4, 100, 2, name = 'fc5')
    print("fc4: ")
    print(fc4.shape)
    print("fc5: ")
    print(self.fc5.shape)
    print("======================")    


    self.dimension['fc4'] = [pool3.shape[1].value*pool3.shape[2].value*64,100]

    self.dimension['fc5'] = [100,2]
    # # 4th Layer: Conv (w ReLu) splitted into two groups
    # conv4 = conv(conv3, 3, 3, 384, 1, 1, groups = 2, name = 'conv4')
  
    # # 5th Layer: Conv (w ReLu) -> Pool splitted into two groups
    # conv5 = conv(conv4, 3, 3, 256, 1, 1, groups = 2, name = 'conv5')
    # pool5 = max_pool(conv5, 3, 3, 2, 2, padding = 'VALID', name = 'pool5')
  
    # 6th Layer: Flatten -> FC (w ReLu) -> Dropout
    # flattened = tf.reshape(pool5, [-1, 6*6*256])
    # fc6 = fc(flattened, 6*6*256, 4096, name='fc6')
    # dropout6 = dropout(fc6, self.KEEP_PROB)
  
    # 7th Layer: FC (w ReLu) -> Dropout

  
    # 8th Layer: FC and return unscaled activations
    # # (for tf.nn.softmax_cross_entropy_with_logits)
    # self.fc8 = fc(dropout7, 4096, self.NUM_CLASSES, relu = False, name='fc8')

  def load_initial_weights(self,session):


    # for layer in self.layerlist:
    #   data = np.random.normal(0,0.0001,(5,5,3,self.dimension['conv1'][3].value))
    
    # with tf.variable_scope('conv1', reuse = True):
    #   var = tf.get_variable('weights',trainable = False)
    #   session.run(var.assign(data))
    # for layer in self.layerlist:
    #   self.weights_paramdict[layer] = tf.get_variable(name=layer,shape=[])

    for layer in self.layerlist:
      with tf.variable_scope(layer, reuse = True):
        if layer[:4]=='conv2':
          data = np.random.normal(0,0.01,(self.dimension[layer][0],self.dimension[layer][1],self.dimension[layer][2],self.dimension[layer][3]))
        elif layer[:2] == 'fc':
          data = np.random.normal(0,0.0001,(self.dimension[layer][0],self.dimension[layer][1]))
        else:
          data = np.random.normal(0,0.0001,(self.dimension[layer][0],self.dimension[layer][1],self.dimension[layer][2],self.dimension[layer][3]))
        var = tf.get_variable('weights',trainable = False)
        session.run(var.assign(data))

    # pass

    # # Load the weights into memory
    # weights_dict = np.load(self.WEIGHTS_PATH, encoding = 'bytes').item()
    # print len(weights_dict['fc8'][0][0])
    # # # Loop over all layer names stored in the weights dict
    # for op_name in weights_dict:
  
    #   # Check if the layer is one of the layers that should be reinitialized
    #   if op_name not in self.SKIP_LAYER:
  
    #     with tf.variable_scope(op_name, reuse = True):
  
    #       # Loop over list of weights/biases and assign them to their corresponding tf variable
    #       for data in weights_dict[op_name]:
  
    #         # Biases
    #         if len(data.shape) == 1:
  
    #           var = tf.get_variable('biases', trainable = False)
    #           session.run(var.assign(data))
  
    #         # Weights
    #         else:
  
    #           var = tf.get_variable('weights', trainable = False)
    #           session.run(var.assign(data))

def conv(x, filter_height, filter_width, num_filters, stride_y, stride_x, name,
         padding='SAME', groups=1):

  # Get number of input channels
  input_channels = int(x.get_shape()[-1])

  # Create lambda function for the convolution
  convolve = lambda i, k: tf.nn.conv2d(i, k,
                                       strides = [1, stride_y, stride_x, 1],
                                       padding = padding)

  with tf.variable_scope(name) as scope:
    # Create tf variables for the weights and biases of the conv layer
    weights = tf.get_variable('weights',
                              shape = [filter_height, filter_width,
                              input_channels/groups, num_filters])
    biases = tf.get_variable('biases', shape = [num_filters])


    if groups == 1:
      conv = convolve(x, weights)

    # In the cases of multiple groups, split inputs & weights and
    else:
      # Split input and weights and convolve them separately
      input_groups = tf.split(axis = 3, num_or_size_splits=groups, value=x)
      weight_groups = tf.split(axis = 3, num_or_size_splits=groups, value=weights)
      output_groups = [convolve(i, k) for i,k in zip(input_groups, weight_groups)]

      # Concat the convolved output together again
      conv = tf.concat(axis = 3, values = output_groups)

    # Add biases
    bias = tf.reshape(tf.nn.bias_add(conv, biases), conv.get_shape().as_list())

    # Apply relu function
    relu = tf.nn.relu(bias, name = scope.name)

    return relu

def fc(x, num_in, num_out, name, relu = True):
  with tf.variable_scope(name) as scope:

    # Create tf variables for the weights and biases
    weights = tf.get_variable('weights', shape=[num_in, num_out], trainable=True)
    biases = tf.get_variable('biases', [num_out], trainable=True)

    # Matrix multiply weights and inputs and add bias
    act = tf.nn.xw_plus_b(x, weights, biases, name=scope.name)

    if relu == True:
      # Apply ReLu non linearity
      relu = tf.nn.relu(act)
      return relu
    else:
      return act

def max_pool(x, filter_height, filter_width, stride_y, stride_x,
             name, padding='SAME'):
  return tf.nn.max_pool(x, ksize=[1, filter_height, filter_width, 1],
                        strides = [1, stride_y, stride_x, 1],
                        padding = padding, name = name)

def avg_pool(x, filter_height, filter_width, stride_y, stride_x,
             name, padding='SAME'):
  return tf.nn.avg_pool(x, ksize=[1, filter_height, filter_width, 1],
                        strides = [1, stride_y, stride_x, 1],
                        padding = padding, name = name)

def lrn(x, radius, alpha, beta, name, bias=1.0):
  return tf.nn.local_response_normalization(x, depth_radius = radius,
                                            alpha = alpha, beta = beta,
                                            bias = bias, name = name)

def dropout(x, keep_prob):
  return tf.nn.dropout(x, keep_prob)


