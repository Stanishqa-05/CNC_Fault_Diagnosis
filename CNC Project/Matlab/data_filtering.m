clc; clear; close all;

% Use SAME path logic as before
file_path = fullfile(getenv('USERPROFILE'), 'Desktop', 'noisy_data.xlsx');

% Read Excel
[num, txt, raw] = xlsread(file_path);

% Extract columns
Time = num(:,1);
Load = num(:,2);
Speed = num(:,3);
Current = num(:,4);
Power = num(:,5);

% Filtering (moving average using filter for old MATLAB)
window = 5;
Load_f = filter(ones(1,window)/window, 1, Load);
Speed_f = filter(ones(1,window)/window, 1, Speed);
Current_f = filter(ones(1,window)/window, 1, Current);
Power_f = filter(ones(1,window)/window, 1, Power);

% Combine
filtered = [Time, Load_f, Speed_f, Current_f, Power_f];

% Header
header = {'Time', 'Load', 'Speed', 'Current', 'Power'};

% Save filtered dataset
save_path = fullfile(getenv('USERPROFILE'), 'Desktop', 'filter_data.xlsx');
writecell([header; num2cell(filtered)], save_path);
disp('Filtered dataset saved to Desktop');