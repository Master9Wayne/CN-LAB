import org.arl.fjage.*
import org.arl.unet.*

/**
 * Receives Protocol.USER datagrams, uppercases the payload, appends the
 * reception time, and replies to the originating node using Protocol.DATA.
 */
class EchoAgent extends UnetAgent {

  @Override
  void startup() {
    subscribe topic(Topics.DATAGRAM)
    log.info('EchoAgent started')
  }

  @Override
  void processMessage(Message msg) {
    if (msg instanceof DatagramNtf && msg.protocol == Protocol.USER) {
      String received = new String(msg.data)
      String replyText = received.toUpperCase() +
        ' @ ' + System.currentTimeMillis()

      send new DatagramReq(
        recipient: msg.sender,
        to: msg.from,
        protocol: Protocol.DATA,
        data: replyText.bytes
      )

      log.info("Echoed '${received}' as '${replyText}'")
    }
  }
}
