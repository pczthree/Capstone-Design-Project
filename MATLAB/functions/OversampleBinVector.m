function [ K ] = OversampleBinVector( A, N )
%OversampleBinVector Takes a 1xN vector A and oversamples it at two samples
%per bit, storing and returning the results in K.

B = 1.+zeros(N,1);
K = kron(A,B);
K = transpose(K(:));

end

