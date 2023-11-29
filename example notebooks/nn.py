from NumPyNet.network import Network
from NumPyNet.layers.connected_layer import Connected_layer
from NumPyNet.layers.cost_layer import Cost_layer
from NumPyNet.layers.cost_layer import cost_type
from NumPyNet.metrics import mean_accuracy_score
from NumPyNet.optimizer import Adam, SGD, Momentum
from NumPyNet.metrics import mean_absolute_error
import numpy as np

print("nn",0,0,2)

class NumpyNetTable(object):
    
    def __init__(self,state_to_X,all_moves,model_dict,verbose=False,save_data=False,
            **kwargs):
        self.all_moves=all_moves
        self.verbose=verbose
        self.save_data=save_data
        self.state_to_X = state_to_X
        if self.save_data:
            self.data=[]

        self._model=None
        self.model_dict=model_dict

        
    @property
    def weights(self):
        W=[]
        for layer in self.model._net:
            try:
                w,b = layer.weights,layer.bias
                W.append(w)
            except AttributeError:  # Cost and input layers don't have weights
                pass
        return W

    @property
    def biases(self):
        B=[]
        for layer in self.model._net:
            try:
                w,b = layer.weights,layer.bias
                B.append(w)
            except AttributeError:  # Cost and input layers don't have weights
                pass
        return B

    @property
    def intercepts(self):
        return self.biases
    

    @property
    def model(self):
        if self._model is None:
            self._model = Network(batch=1, input_shape=(1,1,self.model_dict['input']))

            hidden=self.model_dict.get('hidden',[])
            for n,typ in hidden:
                self._model.add(Connected_layer(outputs=n, activation=typ))

            n,typ=self.model_dict['output']
            self._model.add(Connected_layer(outputs=n, activation=typ))
            self._model.add(Cost_layer(cost_type=self.model_dict['cost']))
            self._model.compile(optimizer=Adam(), metrics=[mean_absolute_error])
            if self.verbose:
                self._model.summary()

        return self._model

    
    def output(self, state):
        from NumPyNet.exception import NetworkError        
        X=self.state_to_X(state)
        if self.verbose:
            print("X",X)
            

        # Reshape the data according to a 4D tensor
        num_samples, size = X.shape
        X = X.reshape(num_samples, 1, 1, size)
        self.model.batch=num_samples

        try:
            _=self.model.predict(X=X,verbose=False)
        except NetworkError:  # not fit
            y=np.zeros(len(self.all_moves))
            self.model.batch=1
            self.model.fit(X=X, y=y, max_iter=1,verbose=self.verbose)  # find some way to make the learning zero here, but it probably won't have a huge effect anyway           
            _=self.model.predict(X=X,verbose=False)

        out=[]
        for layer in self.model:  # no input or cost 
            if isinstance(layer,Connected_layer):
                out.append(layer.output[:].squeeze())


        return out

  
    def __getitem__(self, key):
        if self.verbose:
            print("Getting ",key)
        #X=state_to_X(key)
        #return self.mlp._predict(X)

        if self.all_moves is None:  # first time calling
            self.all_moves=all_possible_moves()


        y=self.output(key)[-1].ravel()        

        T=Table()
        for a,action in enumerate(self.all_moves):
            T[action]=y[a]

        return T

    def __setitem__(self, key, value):
        if self.verbose:
            print("Setting ",key,value)
        X=self.state_to_X(key)

        if isinstance(value,Table):
            arr_value=np.zeros(len(self.all_moves))
            for a,action in enumerate(self.all_moves):
                arr_value[a]=value[action]
        else:
            arr_value=value

        y=np.array([arr_value])
        if self.verbose:
            print("\tX ",X)
            print("\ty ",y)
            
        if self.save_data:
            try:
                output_before=deepcopy(self[key])
            except AttributeError:  # first time
                output_before=None
            
            self.data.append({'X':deepcopy(X),'y':deepcopy(y),'before':output_before})
            
        # Reshape the data according to a 4D tensor
        num_samples, size = X.shape
        X = X.reshape(num_samples, 1, 1, size)
        self.model.batch=num_samples
        self.model.fit(X=X, y=y, max_iter=1,verbose=self.verbose)  # find some way to make the learning zero here, but it probably won't have a huge effect anyway           

        if self.save_data:
            output_after=deepcopy(self[key])
            self.data[-1]['after']=output_after
            



















from sklearn.neural_network import MLPRegressor
import numpy as np
from copy import deepcopy
from Game import Table

class MLPRegressorOverride(MLPRegressor):
# Overriding _init_coef method

   def _init_coef(self, fan_in, fan_out):
        # Use the initialization method recommended by
        # Glorot et al.
        factor = self.initial_weight_factor
        if self.activation == 'logistic':
            factor = factor/3.0

        init_bound = np.sqrt(factor / (fan_in + fan_out))

        # Generate weights and bias:
        coef_init = self._random_state.uniform(-init_bound, init_bound,
                                               (fan_in, fan_out))
        intercept_init = self._random_state.uniform(-init_bound, init_bound,
                                                    fan_out)

        #print("Setting weights (%d,%d) between %g and %g" % (fan_in,fan_out,-init_bound, init_bound))

        return coef_init, intercept_init


class NNTable(object):
    
    def __init__(self,state_to_X,all_moves,verbose=False,save_data=False,activation='tanh',
                 hidden_layer_sizes=(3,),learning_rate=0.01,initial_weight_factor=6.,**kwargs):
        self.all_moves=all_moves
        
        self.mlp = MLPRegressorOverride(solver='sgd', activation=activation,
                                hidden_layer_sizes=hidden_layer_sizes,
                                random_state=1, 
                                learning_rate_init=learning_rate,**kwargs)
        self.mlp.initial_weight_factor=initial_weight_factor
        self.learning_rate=learning_rate
        
        self.verbose=verbose
        self.save_data=save_data
        self.state_to_X = state_to_X
        if self.save_data:
            self.data=[]
        
    @property
    def learning_rate(self):
        return self.mlp.learning_rate_init

    @learning_rate.setter
    def learning_rate(self,value):
        self.mlp.learning_rate_init=value
        
    @property
    def weights(self):
        return self.mlp.coefs_
    @property
    def intercepts(self):
        return self.mlp.intercepts_
    
    
    def output(self,state):
        
        X=self.state_to_X(state)
        if self.verbose:
            print("X",X)
            
        clf=self.mlp
        hidden_layer_sizes = clf.hidden_layer_sizes
        if not hasattr(hidden_layer_sizes, "__iter__"):
            hidden_layer_sizes = [hidden_layer_sizes]
        hidden_layer_sizes = list(hidden_layer_sizes)
        layer_units = [X.shape[1]] + hidden_layer_sizes + \
            [clf.n_outputs_]
        activations = [X]
        for i in range(clf.n_layers_ - 1):
            activations.append(np.empty((X.shape[0],
                                         layer_units[i + 1])))
        clf._forward_pass(activations)

        return activations[1:]
        
    def __getitem__(self, key):
        if self.verbose:
            print("Getting ",key)
        #X=state_to_X(key)
        #return self.mlp._predict(X)

        if self.all_moves is None:  # first time calling
            Q.all_moves=all_possible_moves()


        try:
            y=self.output(key)[-1].ravel()
        except AttributeError:  #not initialized
            X=self.state_to_X(key)
            arr_value=[0]*len(self.all_moves)
            y=np.array([arr_value])

            self.mlp.partial_fit(X, y) 

            y=self.output(key)[-1].ravel()
        

        T=Table()
        for a,action in enumerate(self.all_moves):
            T[action]=y[a]

        return T

    def __setitem__(self, key, value):
        if self.verbose:
            print("Setting ",key,value)
        X=self.state_to_X(key)

        if isinstance(value,Table):
            arr_value=np.zeros(len(self.all_moves))
            for a,action in enumerate(self.all_moves):
                arr_value[a]=value[action]
        else:
            arr_value=value

        y=np.array([arr_value])
        if self.verbose:
            print("\tX ",X)
            print("\ty ",y)
            
        if self.save_data:
            try:
                output_before=deepcopy(self[key])
            except AttributeError:  # first time
                output_before=None
            
            self.data.append({'X':deepcopy(X),'y':deepcopy(y),'before':output_before})
            
        self.mlp.partial_fit(X, y)    
        
        if self.save_data:
            output_after=deepcopy(self[key])
            self.data[-1]['after']=output_after
            