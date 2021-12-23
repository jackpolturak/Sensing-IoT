clear all
%% CSV READ

T = readmatrix('data.csv');

%INPUTS: Danceability, energy, key, loudness, mode, speechiness,
%acouasticness, instumentallness, liveness, valence, tempo:
inputs = T(1:803, [6,7,8,9,10,11,12,13,14,15,16]);

%OUTPUT: Heartrate
output_heartrate = T(1:803, 17);


%%  Linear Regression Meta Model For Heartrate

%Shuffle Data
rng(1);                             % MATLAB random seed 1
newInd = randperm(length(output_heartrate));  % New index order for data sets

inputs_shuffle = inputs(newInd,:);       
output_heartrate_shuffle = output_heartrate(newInd);  

% SPLIT DATA SETS (75%-25% RULE) & NORMALIZE WRT TRAINING SET
splitPt1 = floor(0.75*length(output_heartrate_shuffle));  % Case 1 split point

% Normalization of training data sets
[inputs_train_normalized,PS_inputs_train] = mapstd(inputs_shuffle(1:splitPt1,:)');
[output_train_normalized, PS_output_train] = mapstd(output_heartrate_shuffle(1:splitPt1)');

% Normalization of test data sets
inputs_test_normalized = mapstd('apply',inputs_shuffle(splitPt1+1:end,:)',PS_inputs_train);
output_test_normalized = mapstd('apply',output_heartrate_shuffle(splitPt1+1:end)',PS_output_train);

% FINDING BETA VALUES
heartrate_betas = mvregress(inputs_train_normalized',output_train_normalized');


rsq = 1 - norm(inputs_test_normalized'*heartrate_betas - output_test_normalized')^2/norm(output_test_normalized-mean(output_test_normalized))^2;

%% Polynomial Regression Meta Model For Heartrate

hearate_model = polyfitn(inputs_train_normalized',output_train_normalized','constant x(1) x(2) x(3) x(4) x(1)^2 x(2)^2 x(3)^2 x(4)^2');

%%  Visualising the data

figure(1)

danceability = inputs(:,1);
energy = inputs(:,2);
key = inputs(:,3);
loudness = inputs(:,4);
mode = inputs(:,5);
speechiness = inputs(:,6);
acousticness = inputs(:,7);
instramentalness = inputs(:,8);
liveness = inputs(:,9);
valence = inputs(:,10);
tempo = inputs(:,11);


scatter(loudness, output_heartrate);
