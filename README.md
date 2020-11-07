# python-omnicorelib

```
pip install python-omnicorelib
```

This python library provides an interface to the bitcoind fork omnicore.

This library provides an easy interface to the bitcoin data
structures and protocol. The approach is low-level and "ground up", with a
focus on providing tools to manipulate the internals of how Bitcoin works.

"The Swiss Army Knife of the Bitcoin protocol." - Wladimir J. van der Laan


## Requirements

    sudo apt-get install libssl-dev

The RPC interface, `omnicore.rpc`, is designed to work with Bitcoin Core v0.16.0.
Older versions may work but there do exist some incompatibilities.


## Structure

Everything consensus critical is found in the modules under bitcoin.core. This
rule is followed pretty strictly, for instance chain parameters are split into
consensus critical and non-consensus-critical.

    omnicore.core            - Basic core definitions, datastructures, and
                              (context-independent) validation
    omnicore.core.key        - ECC pubkeys
    omnicore.core.script     - Scripts and opcodes
    omnicore.core.scripteval - Script evaluation/verification
    omnicore.core.serialize  - Serialization

In the future the bitcoin.core may use the Satoshi sourcecode directly as a
library. Non-consensus critical modules include the following:

    omnicore          - Chain selection
    omnicore.base58   - Base58 encoding
    omnicore.bloom    - Bloom filters (incomplete)
    omnicore.net      - Network communication (in flux)
    omnicore.messages - Network messages (in flux)
    omnicore.rpc      - Bitcoin Core RPC interface support
    omnicore.wallet   - Wallet-related code, currently Bitcoin address and
                       private key support

Effort has been made to follow the Satoshi source relatively closely, for
instance Python code and classes that duplicate the functionality of
corresponding Satoshi C++ code uses the same naming conventions: CTransaction,
CBlockHeader, nValue etc. Otherwise Python naming conventions are followed.


## Mutable vs. Immutable objects

Like the Bitcoin Core codebase CTransaction is immutable and
CMutableTransaction is mutable; unlike the Bitcoin Core codebase this
distinction also applies to COutPoint, CTxIn, CTxOut, and CBlock.


## Endianness Gotchas

Rather confusingly Bitcoin Core shows transaction and block hashes as
little-endian hex rather than the big-endian the rest of the world uses for
SHA256. python-bitcoinlib provides the convenience functions x() and lx() in
bitcoin.core to convert from big-endian and little-endian hex to raw bytes to
accomodate this. In addition see b2x() and b2lx() for conversion from bytes to
big/little-endian hex.


## Module import style

While not always good style, it's often convenient for quick scripts if
`import *` can be used. To support that all the modules have `__all__` defined
appropriately.


# Example Code

See `examples/` directory. For instance this example creates a transaction
spending a pay-to-script-hash transaction output:

    $ PYTHONPATH=. examples/spend-pay-to-script-hash-txout.py
    <hex-encoded transaction>


## Selecting the chain to use

Do the following:

    import omnicore
    omnicore.SelectParams(NAME)

Where NAME is one of 'testnet', 'mainnet', or 'regtest'. The chain currently
selected is a global variable that changes behavior everywhere, just like in
the Satoshi codebase.


## Unit tests

Under bitcoin/tests using test data from Bitcoin Core. To run them:

    python3 -m unittest discover

Alternately, if Tox (see https://tox.readthedocs.org/) is available on your
system, you can run unit tests for multiple Python versions:

    ./runtests.sh

HTML coverage reports can then be found in the htmlcov/ subdirectory.

## Documentation

Sphinx documentation is in the "doc" subdirectory. Run "make help" from there
to see how to build. You will need the Python "sphinx" package installed.

Currently this is just API documentation generated from the code and
docstrings. Higher level written docs would be useful, perhaps starting with
much of this README. Pages are written in reStructuredText and linked from
index.rst.
