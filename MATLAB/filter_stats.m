clear all
close all
clc

Ns = 100;
sens = 0.05

[b, a] = cheby2(2, 20, 0.40);
vars = zeros(2,100);

for i=1:1000
    X = ones(1, Ns);
    WGN = GenerateAWGN(Ns, sens);

    Xn = X + WGN;

    Yn = filter(b, a, Xn);

    vars(1,:) = var(Xn(10:Ns));
    vars(2,:) = var(Yn(10:Ns));
end

Xavg = mean(vars(1,:))
Yavg = mean(vars(2,:))

improvement = (Xavg - Yavg)/Xavg
