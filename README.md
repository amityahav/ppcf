# Privacy Preserving Collaborative Filtering
Mediated Secure Multi-Party Protocols for Collaborative Filtering

Implementation of Erez Shmueli and Tamir Tassa's CF algorithm in a privacy preserving manner as written in their paper:

Erez Shmueli, Tamir Tassa: Mediated Secure Multi-Party Protocols for Collaborative Filtering. (2020)

Setup Guide:

1. `git clone` the repository
2. `cd` to the repo directory
3. run `docker-compose up` (Make sure Docker is up and running)
4. Vendors service is accessible via http://127.0.0.1:5003,
   Mediator service is accessible via http://127.0.0.1:5004
   
  Vendors Service API endpoints:
  
  - `/start` - Starting Offline phase of the Algorithm (Model Construction) 
  - `/predict` - for a given vendor id, user id, and item id, returns a prediction for this user rating of the item
  - `/most_recommended` - for a given vendor id and user id, returns the h-most recommended items for this specific user
  - `/error` - calculating Mean Absolute Error over the u1.test test set (located in vendors/app/data/raw_data)
  
  Model was already computed locally on the MovieLen-100k dataset ,80/20 spllit, and used in both services.
  - for a fresh computation of the Model this 3 lines inside the Vendors Dockerfile needs to be commented out:
```sh
COPY app/data/similarity_matrix.npy ppcf/mediator/app/data
COPY app/data/encrypted_mask.npy ppcf/mediator/app/data
COPY app/data/encrypted_user_item_matrix.npy ppcf/mediator/app/data
