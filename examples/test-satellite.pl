#!/usr/bin/perl
use strict;
use warnings;
use Bloonix::IO::SIPC;
use JSON;

my $ip = $ARGV[0] || "127.0.0.1";
my $authkey = $ARGV[1] || "abc";

my $io = Bloonix::IO::SIPC->new(
    peeraddr => $ip,
    peerport => 5464,
    use_ssl => "yes",
    ssl_verify_mode => "none",
    recv_timeout => 60
);

$io->connect;

$io->send({
    action => "exec",
    authkey => $authkey,
    data => {
        command => "check-ping",
        timeout => 30,
        command_options => {
            host => "127.0.0.1",
            warning => "5000,33%",
            critical => "8000,66%",
            timeout => 10
        }
    }
});

my $res = $io->recv;

print JSON->new->pretty->encode($res);
