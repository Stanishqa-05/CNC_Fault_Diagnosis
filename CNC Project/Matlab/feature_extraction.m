clc; clear; close all;

%% LOAD FILTERED DATA
file_path = fullfile(getenv('USERPROFILE'), 'Desktop', 'filter_data.xlsx');
[num, txt, raw] = xlsread(file_path);

% Extract columns
Time = num(:,1);
Load = num(:,2);
Speed = num(:,3);
Current = num(:,4);
Power = num(:,5);

%% PARAMETERS
window = 10;
N = length(Time);
features = [];

for i = 1:N-window+1
    %% FEATURE EXTRACTION (SLIDING WINDOW)
    % Window data
    L = Load(i:i+window-1);
    S = Speed(i:i+window-1);
    C = Current(i:i+window-1);
    P = Power(i:i+window-1);

    % ---- FEATURES ----
    % Mean
    mean_L = mean(L);
    mean_S = mean(S);
    mean_C = mean(C);
    mean_P = mean(P);

    % RMS
    rms_L = sqrt(mean(L.^2));
    rms_S = sqrt(mean(S.^2));
    rms_C = sqrt(mean(C.^2));
    rms_P = sqrt(mean(P.^2));

    % Energy
    energy_L = sum(L.^2);
    energy_S = sum(S.^2);
    energy_C = sum(C.^2);
    energy_P = sum(P.^2);

    % Standard Deviation
    std_L = std(L);
    std_S = std(S);
    std_C = std(C);
    std_P = std(P);

    % Combine into one row (Added missing commas)
    row = [mean_L, mean_S, mean_C, mean_P, ...
           rms_L, rms_S, rms_C, rms_P, ...
           energy_L, energy_S, energy_C, energy_P, ...
           std_L, std_S, std_C, std_P];

    features = [features; row];
end

%% SAVE FEATURE DATASET
header = {'mean_L', 'mean_S', 'mean_C', 'mean_P', ...
          'rms_L', 'rms_S', 'rms_C', 'rms_P', ...
          'energy_L', 'energy_S', 'energy_C', 'energy_P', ...
          'std_L', 'std_S', 'std_C', 'std_P'};

save_path = fullfile(getenv('USERPROFILE'), 'Desktop', 'features_data.xlsx');
writecell([header; num2cell(features)], save_path);
disp('Feature extraction completed');