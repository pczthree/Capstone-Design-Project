%% filter_test.m
% Generates simulated input signal w/ noise, filters it, then shows output
% X --> H --> Y

clear all;
close all;
clc

%% Define project variables
Ns = 10;
Rs = 10;
sens = 0.01; %multiply the noise amplitude

figCount = 1;

%% Generate input vector and add noise
X = OversampleBinVector(round(rand(1,Ns)),Rs);
%X = OversampleBinVector(GenerateBinVector(Ns),Rs);
wgn = GenerateAWGN(Ns*Rs, sens);
Xn = X + wgn;

figure(figCount); figCount = figCount + 1;
stem(X)
title('Input Without Noise', 'FontSize', 18);
axis([-Inf, Inf, -0.5, 1.5]);
set(gca, 'FontSize', 15);

figure(figCount); figCount = figCount + 1;
stem(Xn)
title('Input With WGN', 'FontSize', 18);
axis([-Inf, Inf, -0.5, 1.5]);
set(gca, 'FontSize', 15);

%% Generate filter coefficients
% [b1, a1] = butter(4, 0.4);
[b2, a2] = cheby2(2, 20, 0.40);

% figure(figCount); figCount = figCount + 1;
% freqz(b1, a1);
% figure(figCount); figCount = figCount + 1;
% stepz(b1, a1);
% title('Butterworth Step Response', 'FontSize', 18);
% set(gca, 'FontSize', 15);
% grid on;

figure(figCount); figCount = figCount + 1;
freqz(b2, a2);
figure(figCount); figCount = figCount + 1;
stepz(b2, a2);
% fvtool(b2, a2);
title('Chebyshev II Step Response', 'FontSize', 18);
set(gca, 'FontSize', 15);
grid on;


% Yb = filter(b1, a1, X);
% Ybn = filter(b1, a1, Xn);
Yc = filter(b2, a2, X);
Ycn = filter(b2, a2, Xn);

% figure(figCount); figCount = figCount + 1;
% stem(Yb)
% title('Butterworth Output Without Noise', 'FontSize', 18);
% axis([-Inf, Inf, -1.5, 1.5]);
% set(gca, 'FontSize', 15);
% figure(figCount); figCount = figCount + 1;
% stem(Ybn)
% title('Butterworth Output With WGN', 'FontSize', 18);
% axis([-Inf, Inf, -1.5, 1.5]);
% set(gca, 'FontSize', 15);
% 
figure(figCount); figCount = figCount + 1;
stem(Yc)
title('Chebyshev II Output Without Noise', 'FontSize', 18);
axis([-Inf, Inf, -0.5, 1.5]);
set(gca, 'FontSize', 15);
figure(figCount); figCount = figCount + 1;
stem(Ycn)
title('Chebyshev II Output With WGN', 'FontSize', 18);
axis([-Inf, Inf, -0.5, 1.5]);
set(gca, 'FontSize', 15);