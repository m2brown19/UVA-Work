class MetasploitModule < Msf::Auxiliary
	include Msf::Exploit::Remote::Tcp
	include Msf::Auxiliary::Fuzzer

	def initialize(info = {})
		super(update_info(info,
			'Name' => 'Sync breeze Fuzzer',
			'Description' => %q{Sync Breeze App Fuzzer},
			'Author' => [ 'Michael Brown' ],
			'License' => MSF_LICENSE,
			'Version' => '$Revision: 1 $'
		))

		register_options([
			Opt::RPORT(80),
			OptString.new("USERNAME", [true, "the username to log in with"]),
			OptString.new("PASSWORD", [true, "password to log in with"]),
			OptString.new("TARGETURI", [true, "uri of victim", "/login"]),
			OptString.new("VHOST", [false, "The virtual host name to use in requests"]),
			OptString.new("URIBASE", [true, "The base URL to use for the request fuzzer", "target.example.com"]),
		])
	end

	def do_http_get(uri='',opts={})
		@connected = false
		connect
		@connected = true

		sock.put("GET #{uri} HTTP/1.1\r\nHost: #{datastore['VHOST'] || rhost}\r\n\r\n")
		sock.get_once(-1, opts[:timeout] || 0.01)
	end

	def fuzz_str()
		return Rex::Text.rand_text_alphanumeric(rand(2000))
	end

	def run()
		srand(0)
		connect

		rhost = datastore['RHOST']
		
		
	end
end