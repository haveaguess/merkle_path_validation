
# Assumptions


It is assumed there is a typo in the specification and that this sentance in the spec is supposed
to end "in the next operation":

    The output of each operation is `Operator(Prefix + message + Postfix)`, which will
    become the message in the operation

It is assumed that the `+` operator above is just string concatenation

It is assumed that json file contains arrays of arrays of length 3 containing fields: `operator, prefix, postfix`



# Implementation notes

Written to run against Python 2

I normally follow PEP8 style guide:

https://www.python.org/dev/peps/pep-0008/

.. but the code was already non-conforming as it uses CamelCase for VerifyHash function, so I 
continued to follow your existing style

Originally did all the concatenations pre-hash as little-endian (since many examples of Merkle tree/proof work were doing similar online)
but then after lots of frustration I found this implementation in github that exactly matches the problem and they
were doing all their work in big-endian : https://github.com/aliminaei/merkle_tree_verify/blob/master/main.py





# Background reading on Merkle paths/proofs


- https://medium.com/coinmonks/how-to-manually-verify-the-merkle-root-of-a-bitcoin-block-command-line-7881397d4db1 implies sha256 is applied twice ?! 
- https://medium.com/hackergirl/how-to-calculate-the-hash-of-a-block-in-bitcoin-8f6aebb0dc6d again applies sha256 twice
- https://bitcoin.stackexchange.com/questions/50674/why-is-the-full-merkle-path-needed-to-verify-a-transaction
- https://medium.com/@jgm.orinoco/understanding-merkle-pollards-1547fc7efaa


