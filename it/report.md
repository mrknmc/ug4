---
title: 'Information Theory Assignment'
author: 's1140740'
---

# Source Coding

## Character Statistics

The entropy $H(X_n)$ is 4.168.

## Bigram Statistics

 a. The joint entropy $H(X_n, X_{n+1})$ is 7.572.
 b. Because they are not i.i.d.
 c. The conditional entropy $H(X_{n+1} \mid X_n) = H(X_n, X_{n+1}) - H(X_n)$ is 3.404.

## Compression with known distributions

We know that the message length is always within two bits of the Shannon information content [^1] and thus the maximum number of bits is computed as:

$$\Big{\lceil} h(x) \Big{\rceil} + 2 = \Bigg{\lceil} -\sum_{n = 1}^{N}{\log_2{P(x_n)}}\Bigg{\rceil} + 2$$

where $x_n$ is the $n$-th character in the file and $N$ is the length of the file. Probabilities from question 1 are used.

The maximum number of bits an arithmetic coder would use to represent `thesis.txt` assuming this model is therefore 1,433,836.

---

The maximum number of bits an arithmetic coder would use to represent `thesis.txt` assuming the more sophisticated model is 1,171,194. The length is computed as:

$$\Bigg{\lceil} - \log_2{P(x_1)} - \sum_{n = 1}^{N}{\log_2{\frac{P(x_{n+1}, x_n)}{P(x_n)}}} \Bigg{\rceil} + 2 = \Bigg{\lceil} - \log_2{P(x_1)} - \sum_{n = 1}^{N}{\log_2{P(x_{n+1} | x_n)}} \Bigg{\rceil} + 2$$

The joint probabilities from question 2 are combined together with probabilities from question 1 to compute the conditional probabilities which are used in chain rule.

## Compression with limited precision header

Assuming we transmit the powers of 2 required to get back the original probabilities, we require 8 bits per character. Since our alphabet is of size 27 (`'a'` - `'z'` and `' '`) we require $27 * 8 = 216$ bits for the header if we send the powers ordered alphabetically with space at the end.

Furthermore, the probabilities are re-normalised before use (by both sender and receiver) to add up to 1 and then applied in the same fashion as in the previous question to compute the maximum number of bits required. Thus we need 1,435,081 bits for data and 1,435,297 bits altogether with this scheme.

---

**TODO!**

## Compression with adaptation

Using the Laplace prediction rule for the i.i.d. model the maximum number of bits required to encode `thesis.txt` is 1,434,027.

The rule is computed for every character of the file and these probabilities are then used to compute the Shannon information content. We then take the ceiling and add 2.

---

Using the prediction rule for the bigram model the maximum number of bits required to encode `thesis.txt` is 1,175,382.

Again the rule is computed for every character of the file and the probabilities are then used to compute the Shannon information content. Again, we take the ceiling and add 2.

# Noisy Channel Coding

## XOR-ing packets

The resulting string is `User: s5559183948`.

## Decoding packets from a digital fountain

The algorithm takes as its input a list of packets and a list of sets containing identities of the source bytes that were used for each of the packets.

It loops through these lists zipped and only breaks out if all sets of identities are empty. Every time it encounters a set in position $i$ with only one identity number $k$ it pops $k$ from the set and saves the character represented by the $i$-th packet in ASCII in the $k$-th position of the result list.

After this, $k$ is removed from all the other sets that contain it. Furthermore, if any of these sets, say in position $j$, contains other numbers as well then the $i$-th packet is XOR'd with the packet in $j$-th position.

The source string is then re-constructed from the result list. The packets used to construct the string are also recorded and returned with the string.

The decoded string is `Password: X!3baA1z` and packets used are as follows: `16`, `23`, `2`, `21`, `22`, `20`, `8`, `10`, `17`, `19`, `6`, `7`, `9`, `11`, `14`, `15`, `12`, `13`. 

## Creating a code

I re-implemented the 2-dimensional parity-check code. It transforms a sequence of 16 source bits into a sequence of 24 bits, thus it is a (24, 16) block code. An $n$-dimensional parity-check code can correct $n/2$ errors. Thus this code can only correct bit sequences with 1 error.

### Encoding

In the encoding step 8 parity check bits are added on to the source sequence $x_{1} \dotso x_{16}$ computed as follows:

\begin{equation} \label{eq:ys}
    \begin{gathered}
    y_{1} = x_{1} \oplus x_{2} \oplus x_{3} \oplus x_{4} \\
    y_{2} = x_{5} \oplus x_{6} \oplus x_{7} \oplus x_{8} \\
    y_{3} = x_{9} \oplus x_{10} \oplus x_{11} \oplus x_{12} \\
    y_{4} = x_{13} \oplus x_{14} \oplus x_{15} \oplus x_{16}
    \end{gathered}
    \hspace{6em}
    \begin{gathered}
    z_{1} = x_{1} \oplus x_{5} \oplus x_{9} \oplus x_{13} \\
    z_{2} = x_{2} \oplus x_{6} \oplus x_{10} \oplus x_{14} \\
    z_{3} = x_{3} \oplus x_{7} \oplus x_{11} \oplus x_{15} \\
    z_{4} = x_{4} \oplus x_{8} \oplus x_{12} \oplus x_{16}
    \end{gathered}
\end{equation}

The following is then transmitted:

$$x_{1} \; x_{2} \; x_{3} \; x_{4} \; y_{1} \; x_{5} \; x_{6} \; x_{7} \; x_{8} \; y_{2} \; x_{9} \; x_{10} \; x_{11} \; x_{12} \; y_{3} \; x_{13} \; x_{14} \; x_{15} \; x_{16} \; y_{4} \; z_{1} \; z_{2} \; z_{3} \; z_{4}$$

### Decoding

The transmitted message can be represented as:

\begin{center}
    \begin{tabular}{ c | c | c | c || c }
        $x_{1}$ & $x_{2}$ & $x_{3}$ & $x_{4}$ & $y_1$ \\ \hline
        $x_{5}$ & $x_{6}$ & $x_{7}$ & $x_{8}$ & $y_2$ \\ \hline
        $x_{9}$ & $x_{10}$ & $x_{11}$ & $x_{12}$ & $y_3$ \\ \hline
        $x_{13}$ & $x_{14}$ & $x_{15}$ & $x_{16}$ & $y_4$ \\ \hline\hline
        $z_1$ & $z_2$ & $z_3$ & $z_4$ & \\
    \end{tabular}
\end{center}

where every $y_i$ represents the result of applying XOR to the rest of the bits in the same row and every $z_j$ represents the result of applying XOR to the rest of the bits in the same column.

Upon receiving the transmitted message
    
$$x_{1}' \; x_{2}' \; x_{3}' \; x_{4}' \; y_{1}' \; x_{5}' \; x_{6}' \; x_{7}' \; x_{8}' \; y_{2}' \; x_{9}' \; x_{10}' \; x_{11}' \; x_{12}' \; y_{3}' \; x_{13}' \; x_{14}' \; x_{15}' \; x_{16}' \; y_{4}' \; z_{1}' \; z_{2}' \; z_{3}' \; z_{4}'$$

$y_1 - y_4$ and $z_1 - z_4$ are re-computed as in equations \ref{eq:ys} and compared to the corresponding values received. If $y_{i} \neq y_{i}'$ for exactly one $i$ and $z_{j} \neq z_{j}'$ for exactly one $j$ then there was an error in the body of the message in row $i$ and column $j$ and we can correct it.

If only one $y_i$ 

### Example

For example take a source sequence 0100111001010011. We compute $y_1 - y_4$ and $z_1 - z_4$:

\begin{center}
    \begin{tabular}{ c | c | c | c || c }
        0 & 1 & 0 & 0 & 1 \\ \hline
        1 & 1 & 1 & 0 & 1 \\ \hline
        0 & 1 & 0 & 1 & 0 \\ \hline
        0 & 0 & 1 & 1 & 0 \\ \hline\hline
        1 & 1 & 0 & 0 & \\
    \end{tabular}
\end{center}

and transmit 010011110101010001101100.

Let us say that when the decoder receives the message bit in row 2 and column 3 is flipped.

\begin{center}
    \begin{tabular}{ c | c | c | c || c }
        0 & 1 & 0 & 0 & 1 \\ \hline
        1 & 1 & \color{red} 0 & 0 & 1 \\ \hline
        0 & 1 & 0 & 1 & 0 \\ \hline
        0 & 0 & 1 & 1 & 0 \\ \hline\hline
        1 & 1 & 0 & 0 & \\
    \end{tabular}
\end{center}

Now, the decoder re-computes $y_1 - y_4$ and $z_1 - z_4$:

\begin{equation} \label{eq:ys}
    \begin{gathered}
    y_{1} = 1 = 1 = y_{1}' \\
    y_{2} = 0 \neq 1 = y_{2}' \\
    y_{3} = 0 = 0 = y_{3}' \\
    y_{4} = 0 = 0 = y_{4}'
    \end{gathered}
    \hspace{6em}
    \begin{gathered}
    z_{1} = 1 = 1 = z_{1}' \\ 
    z_{2} = 1 = 1 = z_{2}' \\ 
    z_{3} = 1 \neq 0 = z_{3}' \\ 
    z_{4} = 0 = 0 = z_{4}'
    \end{gathered}
\end{equation}

and it can detect and correct the error as it now knows the error is in row 2 and column 3.

Therefore it produces the original message 0100111001010011.
