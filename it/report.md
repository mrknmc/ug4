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

We know that with arithmetic coding the message length is always within two bits of the Shannon information content and thus the maximum number of bits is computed as:

$$\Big{\lceil} h(x) \Big{\rceil} + 2 = \Bigg{\lceil} -\sum_{n = 1}^{N}{\log_2{P(x_n)}}\Bigg{\rceil} + 2$$

where $x_n$ is the $n$-th character in the file and $N$ is the length of the file. Probabilities from question 1 are used.

The maximum number of bits an arithmetic coder would use to represent `thesis.txt` assuming this model is therefore 1,433,836.

---

The maximum number of bits an arithmetic coder would use to represent `thesis.txt` assuming the more sophisticated model is 1,171,194. The length is computed as:

$$\Bigg{\lceil} - \log_2{P(x_1)} - \sum_{n = 1}^{N}{\log_2{P(x_{n+1} | x_n)}} \Bigg{\rceil} + 2 = \Bigg{\lceil} - \log_2{P(x_1)} - \sum_{n = 1}^{N}{\log_2{\frac{P(x_{n+1}, x_n)}{P(x_n)}}} \Bigg{\rceil} + 2$$

The joint probabilities from question 2 are combined together with probabilities from question 1 to compute the conditional probabilities which are used in chain rule.

## Compression with limited precision header

Assuming we transmit the powers of 2 required to get back the original probabilities, we require 8 bits per character. Since our alphabet is of size 27 (`'a'` - `'z'` and `' '`) we require $27 * 8 = 216$ bits for the header if we send the powers ordered alphabetically with space at the end.

Furthermore, the probabilities are re-normalised before use (by both sender and receiver) to add up to 1 and then applied in the same fashion as in the previous question to compute the maximum number of bits required. Thus the maximum number of bits required to encode `thesis.txt` is 1,435,081. Hence, together with the header we require 1,435,297 bits with this scheme.

---

There are two ways to approach this problem. In one solution we could transmit information about the i.i.d. distribution and the joint distribution in the header. These distributions would then be combined to calculate conditional probabilities in the chain rule. Another solution would be to to transmit information about the i.i.d. distribution and the conditional probabilities directly. I chose to implement the second solution as it yielded better results.

Both solutions would require us to put $27 * 8 = 216$ bits about the i.i.d. distribution together with $27 * 27 * 8 = 5,832$ bits about the conditional or joint distribution in the header. Thus altogether we would require 6,048 bits for the header, assuming a 27 letter alphabet and 8 bits per character.

As for the body of the message, we need to re-normalise the conditional probabilities so that:

$$\sum_{i} P(x_{n+1}=a_i|x_n=a_j) = 1$$

Hence, the maximum number of bits required to encode `thesis.txt` is 1,178,320. Thus, together with the header we require 1,184,368 bits with this scheme.

## Compression with adaptation

Using the Laplace prediction rule for the i.i.d. model the maximum number of bits required to encode `thesis.txt` is 1,434,027.

The rule is computed for every character of the file and these probabilities are then used to compute the Shannon information content. We then take the ceiling and add 2 as in the previous question.

---

Using the prediction rule for the bigram model the maximum number of bits required to encode `thesis.txt` is 1,175,382.

Again the rule is computed for every character of the file and the probabilities are then used to compute the Shannon information content. Again, we take the ceiling and add 2 as before.

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

I re-implemented the 2-dimensional parity-check code which is a $(N, K)$ block code. Even though my implementation is generic for any $N$ and $K$, in this report I am going to discuss the performance of an (8, 4) parity-check code. An $n$-dimensional parity-check code can correct $n/2$ errors. Thus this code can only correct bit sequences with 1 error.

### Encoding

In the encoding step 4 parity check bits are added to the source sequence $x_{1} \dotso x_{4}$, computed as follows:

\begin{equation} \label{eq:ys}
    \begin{gathered}
    y_{1} = x_{1} \oplus x_{2}  \\
    y_{2} = x_{3} \oplus x_{4}
    \end{gathered}
    \hspace{6em}
    \begin{gathered}
    z_{1} = x_{1} \oplus x_{3}  \\
    z_{2} = x_{2} \oplus x_{4}
    \end{gathered}
\end{equation}

Following is the message that is then transmitted over the channel:

$$x_{1} \; x_{2} \; y_{1} \; x_{3} \; x_{4} \; y_{2} \; z_{1} \; z_{2}$$

### Decoding

The transmitted message can be represented as:

\begin{center}
    \begin{tabular}{ c | c || c }
        $x_{1}$ & $x_{2}$ & $y_{1}$ \\ \hline
        $x_{3}$ & $x_{4}$ & $y_{2}$\\ \hline \hline
        $z_{1}$ & $z_{2}$ &
    \end{tabular}
\end{center}

where every $y_i$ represents the result of applying XOR to the rest of the bits in row $i$ and every $z_j$ represents the result of applying XOR to the rest of the bits in column $j$.

Upon receiving the transmitted message

$$x_{1}' \; x_{2}' \; y_{1}' \; x_{3}' \; x_{4}' \; y_{2}' \; z_{1}' \; z_{2}'$$

$y_1, y_2, z_1 \text{ and } z_2$ are re-computed as in equations \ref{eq:ys} and compared to the corresponding values received. If $y_{i} \neq y_{i}'$ for exactly one $i$ and $z_{j} \neq z_{j}'$ for exactly one $j$ then there was an error in the body of the message in row $i$ and column $j$ and we can correct it.

In any other case, there is nothing we can do, since we can only correct one error and we do not care about single errors of the parity-check bits.


### Rate

The rate under this code:

$$R = \frac{\log_2{S}}{N} = \frac{K}{N} = \frac{4}{8} = \frac{1}{2}$$

### Bit error probability

I arrived at the following bit error probabilities:

+-------+----------+
|  $f$  |  $p_B$   |
+=======+==========+
|   0.4 | 0.406528 |
+-------+----------+
|   0.1 | 0.059248 |
+-------+----------+
| 0.001 | 0.007976 |
+-------+----------+

These were confirmed analytically, as can be seen in the tests in `test.py`.

### Example

As an example, consider source sequence 0100. We compute $y_1, y_2, z_1 \text{ and } z_2$:

\begin{center}
    \begin{tabular}{ c | c || c }
        0 & 1 & 1 \\ \hline
        0 & 0 & 0 \\ \hline\hline
        0 & 1 & \\
    \end{tabular}
\end{center}

and hence transmit message 01100001.

Let us say that when the decoder receives the message bit in row 2 and column 1 is flipped.

\begin{center}
    \begin{tabular}{ c | c || c }
        0 & 1 & 1 \\ \hline
        \color{red} 1 & 0 & 0 \\ \hline\hline
        0 & 1 & \\
    \end{tabular}
\end{center}

Now, the decoder re-computes $y_1, y_2, z_1 \text{ and } z_4$:

\begin{equation}
    \begin{gathered}
    y_{1} = 1 = 1 = y_{1}' \\
    y_{2} = 1 \neq 0 = y_{2}' \\
    \end{gathered}
    \hspace{6em}
    \begin{gathered}
    z_{1} = 1 \neq 0 = z_{1}' \\ 
    z_{2} = 1 = 1 = z_{2}' \\ 
    \end{gathered}
\end{equation}

and it can detect and correct the error as it now knows the error is in row 2 and column 1.

Therefore it produces the original message 0100.

\newpage

# Code

\lstinputlisting[language=Python]{count.py}

\lstinputlisting[language=Python]{code.py}

\lstinputlisting[language=Python]{flipper.py}

\lstinputlisting[language=Python]{test.py}

