function [ W ] = GenerateAWGN( N, s )
%GenerateAWGN Returns a 1xN gaussian random vector scaled by factor s
%   Detailed explanation goes here

W = s*randn(1,N);

end

