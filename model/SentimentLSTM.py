

import torch.nn as nn

class SentimentLSTM(nn.Module):
    """
    The RNN model that will be used to perform Sentiment analysis.
    """

    def __init__(self, output_size, embedding_dim, hidden_dim, n_layers, n_cell, drop_prob = 0.2):
        """
        Initialize the model by setting up the layers.
        """
        super().__init__()

        self.output_size = output_size
        self.n_layers = n_layers
        self.hidden_dim = hidden_dim
        
        # LSTM layers
        self.lstm = nn.LSTM(input_size = embedding_dim,hidden_size = hidden_dim, num_layers = n_layers, batch_first = True, dropout = drop_prob)
        
        # dropout layer
        self.dropout = nn.Dropout(0.)
        
        # linear and sigmoid layers 
        self.fc = nn.Linear(hidden_dim, output_size)
        #self.fc1 = nn.Linear(hidden_dim, hidden_dim*2)
        #self.relu1 = nn.LeakyReLU()
        #self.fc2 = nn.Linear(hidden_dim*2, output_size)
      
        self.softmax = nn.Softmax(dim = 1)
        

    def forward(self, x, hidden):
        """
        Perform a forward pass of our model on some input and hidden state.
        """
        batch_size = x.size(0)
        #print(x)
        # embeddings and lstm_out
        lstm_out, hidden = self.lstm(x, hidden)
        #print(lstm_out.shape)
        #stack up lstm outputs
        lstm_out = lstm_out.contiguous().view(-1, self.hidden_dim)
        #print(lstm_out.shape)
        
        # dropout and fully-connected layer
        out = self.dropout(lstm_out)
        #print(out.shape)
        #out = lstm_out[:, -1, :]
        #print(out.shape)
        out = self.fc(out)
        #out = self.fc1(out)
        #out = self.fc2(out)
        #print(out.shape)
        #sigmoid function
        #print(out.shape)
        out = out.contiguous().view(batch_size, -1, self.output_size)
        out = out[:, -1, :]
        out = self.softmax(out)
        # reshape to be batch_size first
        #print(out.shape)
        #out = out.view(batch_size,n_cell, -1)
        #print(out.shape)
        #out = out[:, -1] # get last batch of labels
        #print(out.shape)
        # return last sigmoid output and hidden state

        return out, hidden
    
    
    def init_hidden(self, batch_size, train_on_gpu = False):
        ''' Initializes hidden state '''
        # Create two new tensors with sizes n_layers x batch_size x hidden_dim,
        # initialized to zero, for hidden state and cell state of LSTM
        weight = next(self.parameters()).data
        
        if (train_on_gpu):
            hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().cuda(),
                  weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().cuda())
        else:
            hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_(),
                      weight.new(self.n_layers, batch_size, self.hidden_dim).zero_())
        
        return hidden