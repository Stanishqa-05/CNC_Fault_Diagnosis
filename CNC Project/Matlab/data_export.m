clc; clear; close all;

%% PARAMETERS
N = 163;
t = (1:N)';

%% BASE SIGNAL (PHYSICS-BASED)
load_base = 40 + 10*sin(0.1*t); % Load variation
speed_base = 1500 + 30*sin(0.05*t); % Speed variation

% Current depends on load & speed
current_base = 0.05*load_base + 0.002*(2000 - speed_base);

% Power relation
power_base = current_base .* speed_base / 1000;

%% ADD CONTROLLED NOISE
noise_level = 0.05;
load_noisy = load_base + noise_level*randn(N,1)*10;
speed_noisy = speed_base + noise_level*randn(N,1)*20;
current_noisy = current_base + noise_level*randn(N,1);
power_noisy = power_base + noise_level*randn(N,1);

%% COMBINE DATA INTO MATRIX
data = [t, load_noisy, speed_noisy, current_noisy, power_noisy];

%% ADD HEADER (CELL FORMAT)
header = {'Time', 'Load', 'Speed', 'Current', 'Power'};
output = [header; num2cell(data)];

%% SAVE TO DESKTOP
desktop_path = fullfile(getenv('USERPROFILE'), 'Desktop', 'noisy_data.xlsx');
writecell(output, desktop_path); % Modern MATLAB function
disp('File saved successfully on Desktop as noisy_data.xlsx');

%% PLOT FOR VERIFICATION
figure;
plot(t, current_noisy);
title('Noisy Current Signal');
xlabel('Time');
ylabel('Current');
grid on;