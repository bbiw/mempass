
A major problem with passwords is memorizing them.

We can solve the problem of passwords being too short or being shared between
different logins by using a password vault. The problem now becomes how to
protect that vault. In other words, how to I memorize a sufficiently strong
master password that I don't mind having most of my eggs in that basket?

I could write it down. But that creates the risk of someone else finding the
paper and (a) knowing what it represents and opening my vault, or (b) *not*
knowing what it represents and throwing it away. This is obviously not a
long-term solution. Memorizing it is really the only way.

So how do you do that? By typing it hundreds of times. This program offers
a way for you to type a new password hundreds of times, and tracks when you
did it and how quickly you did it and how frequently you made mistakes.

When you start with a new password, you should type it a dozen or so times
immediately. Then wait three minutes and do it again. Then wait five minutes,
and do it again. Then ten minutes. Then fifteen minutes. Then twenty-five
minutes. Then sixty minutes. etc. Each repetition is spaced further from the
previous drill. After the first week, you should have memorized the password
well enough that you won't need any hints, so the program can store a hash of
the password instead of the real thing.

And yes: this process works. I can still remember a 128-bit password that I
memorized over two years ago, even though I rarely use it.

Issues:

 * You will need to store the password on a computer in the beginning.

 * This should be a computer that is never connected to a network.
   (A Raspberry Pi might be a good candidate: you can keep the SD card in
   your wallet or a safe or a safe deposit box.)

 * You should encrypt the file that stores the passwords.

 * Protecting it with an easy to memorize (i.e. weak) password is better than not
   protecting it at all.

 * After a week, you can protect it with a newly-memorized strong password, and
   ensure that any weakly protected files are destroyed.
